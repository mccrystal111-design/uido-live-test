-- Execute after round_persistence_rls_setup.sql and the draft migration.
-- The session simulates one authenticated user. All rejection tests must fail
-- specifically because of RLS; unexpected success or a different SQL error fails QA.

CREATE OR REPLACE FUNCTION public.qa_expect_rls_rejection(statement text, label text)
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
  BEGIN
    EXECUTE statement;
    RAISE EXCEPTION 'FAIL: expected RLS rejection for %', label;
  EXCEPTION
    WHEN insufficient_privilege THEN
      RAISE NOTICE 'PASS: rejected %', label;
  END;
END;
$$;
GRANT EXECUTE ON FUNCTION public.qa_expect_rls_rejection(text, text) TO authenticated;

CREATE OR REPLACE FUNCTION public.qa_expect_check_violation(statement text, label text)
RETURNS void
LANGUAGE plpgsql
AS $
BEGIN
  BEGIN
    EXECUTE statement;
    RAISE EXCEPTION 'FAIL: expected immutable-context rejection for %', label;
  EXCEPTION
    WHEN check_violation THEN
      RAISE NOTICE 'PASS: rejected immutable context change for %', label;
  END;
END;
$;
GRANT EXECUTE ON FUNCTION public.qa_expect_check_violation(text, text) TO authenticated;

SET ROLE authenticated;
SET request.jwt.claim.sub = '00000000-0000-4000-8000-000000000001';

-- Published active course/version with matching tee set is accepted.
DO $$
BEGIN
  INSERT INTO public.uido_rounds (id, user_id, course_id, course_version_id, tee_set_id, status)
  VALUES (
    '50000000-0000-4000-8000-000000000004',
    auth.uid(),
    '10000000-0000-4000-8000-000000000001',
    '20000000-0000-4000-8000-000000000001',
    '30000000-0000-4000-8000-000000000001',
    'started'
  );
  RAISE NOTICE 'PASS: active course + published version + matching tee set accepted';
END $$;

SELECT public.qa_expect_rls_rejection(
  $sql$INSERT INTO public.uido_rounds (id,user_id,course_id,course_version_id,status)
       VALUES ('50000000-0000-4000-8000-000000000005',auth.uid(),
       '10000000-0000-4000-8000-000000000001',
       '20000000-0000-4000-8000-000000000002','started')$sql$,
  'draft course version'
);

SELECT public.qa_expect_rls_rejection(
  $sql$INSERT INTO public.uido_rounds (id,user_id,course_id,course_version_id,status)
       VALUES ('50000000-0000-4000-8000-000000000006',auth.uid(),
       '10000000-0000-4000-8000-000000000001',
       '20000000-0000-4000-8000-000000000003','started')$sql$,
  'course/version mismatch'
);

SELECT public.qa_expect_rls_rejection(
  $sql$INSERT INTO public.uido_rounds (id,user_id,course_id,course_version_id,status)
       VALUES ('50000000-0000-4000-8000-000000000007',auth.uid(),
       '10000000-0000-4000-8000-000000000002',
       '20000000-0000-4000-8000-000000000003','started')$sql$,
  'inactive course'
);

SELECT public.qa_expect_rls_rejection(
  $sql$INSERT INTO public.uido_rounds (id,user_id,course_id,course_version_id,tee_set_id,status)
       VALUES ('50000000-0000-4000-8000-000000000008',auth.uid(),
       '10000000-0000-4000-8000-000000000001',
       '20000000-0000-4000-8000-000000000001',
       '30000000-0000-4000-8000-000000000002','started')$sql$,
  'tee set from another course version'
);

-- A hole row must belong to the user's round and match its version + hole number.
DO $$
BEGIN
  INSERT INTO public.uido_round_holes (id, round_id, hole_id, hole_number)
  VALUES (
    '60000000-0000-4000-8000-000000000004',
    '50000000-0000-4000-8000-000000000001',
    '40000000-0000-4000-8000-000000000001',
    1
  );
  RAISE NOTICE 'PASS: own round + matching hole accepted';
END $$;

SELECT public.qa_expect_rls_rejection(
  $sql$INSERT INTO public.uido_round_holes (id,round_id,hole_id,hole_number)
       VALUES ('60000000-0000-4000-8000-000000000005',
       '50000000-0000-4000-8000-000000000001',
       '40000000-0000-4000-8000-000000000002',2)$sql$,
  'hole from another course version'
);

SELECT public.qa_expect_rls_rejection(
  $sql$INSERT INTO public.uido_round_holes (id,round_id,hole_id,hole_number)
       VALUES ('60000000-0000-4000-8000-000000000006',
       '50000000-0000-4000-8000-000000000001',
       '40000000-0000-4000-8000-000000000003',1)$sql$,
  'hole number mismatch'
);

SELECT public.qa_expect_rls_rejection(
  $sql$INSERT INTO public.uido_round_holes (id,round_id,hole_id,hole_number)
       VALUES ('60000000-0000-4000-8000-000000000007',
       '50000000-0000-4000-8000-000000000002',
       '40000000-0000-4000-8000-000000000001',1)$sql$,
  'another users round'
);

SELECT public.qa_expect_rls_rejection(
  $sql$UPDATE public.uido_round_holes
       SET hole_id='40000000-0000-4000-8000-000000000002', hole_number=2
       WHERE id='60000000-0000-4000-8000-000000000001'$sql$,
  'round-hole update to another course version'
);

SELECT public.qa_expect_check_violation(
  $sql$UPDATE public.uido_rounds
       SET course_version_id='20000000-0000-4000-8000-000000000002'
       WHERE id='50000000-0000-4000-8000-000000000001'$sql$,
  'round course version after creation'
);

-- A shot must reference only the current user's round and its matching hole row.
DO $$
BEGIN
  INSERT INTO public.uido_shots (id,user_id,round_id,round_hole_id,shot_number)
  VALUES (
    '70000000-0000-4000-8000-000000000002',
    auth.uid(),
    '50000000-0000-4000-8000-000000000001',
    '60000000-0000-4000-8000-000000000001',
    2
  );
  RAISE NOTICE 'PASS: shot attached to own round and hole accepted';
END $$;

SELECT public.qa_expect_rls_rejection(
  $sql$INSERT INTO public.uido_shots (id,user_id,round_id,round_hole_id,shot_number)
       VALUES ('70000000-0000-4000-8000-000000000003',auth.uid(),
       '50000000-0000-4000-8000-000000000002',
       '60000000-0000-4000-8000-000000000002',3)$sql$,
  'shot attached to another users round'
);

SELECT public.qa_expect_rls_rejection(
  $sql$INSERT INTO public.uido_shots (id,user_id,round_id,round_hole_id,shot_number)
       VALUES ('70000000-0000-4000-8000-000000000004',auth.uid(),
       '50000000-0000-4000-8000-000000000001',
       '60000000-0000-4000-8000-000000000002',4)$sql$,
  'shot round/hole mismatch'
);

SELECT public.qa_expect_rls_rejection(
  $sql$INSERT INTO public.uido_shots (id,user_id,round_id,round_hole_id,shot_number)
       VALUES ('70000000-0000-4000-8000-000000000005',auth.uid(),
       NULL,'60000000-0000-4000-8000-000000000001',5)$sql$,
  'shot hole reference without round reference'
);

SELECT public.qa_expect_rls_rejection(
  $sql$UPDATE public.uido_shots
       SET round_id='50000000-0000-4000-8000-000000000002'
       WHERE id='70000000-0000-4000-8000-000000000001'$sql$,
  'shot update to another users round'
);

RESET ROLE;
