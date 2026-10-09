-- Local PostgreSQL fixture for testing the draft round-persistence RLS migration.
-- This schema is deliberately minimal and is never connected to Supabase production.

DO $$
BEGIN
  CREATE ROLE anon NOLOGIN;
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
  CREATE ROLE authenticated NOLOGIN;
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

CREATE SCHEMA IF NOT EXISTS auth;
CREATE OR REPLACE FUNCTION auth.uid()
RETURNS uuid
LANGUAGE sql
STABLE
AS $$
  SELECT nullif(current_setting('request.jwt.claim.sub', true), '')::uuid
$$;
GRANT USAGE ON SCHEMA auth TO authenticated;
GRANT EXECUTE ON FUNCTION auth.uid() TO public;

CREATE TABLE public.courses (
  id uuid PRIMARY KEY,
  status text NOT NULL
);
CREATE TABLE public.course_versions (
  id uuid PRIMARY KEY,
  course_id uuid NOT NULL REFERENCES public.courses(id),
  status text NOT NULL
);
CREATE TABLE public.tee_sets (
  id uuid PRIMARY KEY,
  course_version_id uuid NOT NULL REFERENCES public.course_versions(id)
);
CREATE TABLE public.course_holes (
  id uuid PRIMARY KEY,
  course_version_id uuid NOT NULL REFERENCES public.course_versions(id),
  hole_number integer NOT NULL
);
CREATE TABLE public.uido_rounds (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL,
  course_id uuid NOT NULL REFERENCES public.courses(id),
  course_version_id uuid NOT NULL REFERENCES public.course_versions(id),
  tee_set_id uuid REFERENCES public.tee_sets(id),
  round_type text NOT NULL DEFAULT 'scored',
  status text NOT NULL DEFAULT 'started',
  started_at timestamptz NOT NULL DEFAULT now(),
  ended_at timestamptz,
  start_location text,
  course_selection_method text,
  device_context jsonb NOT NULL DEFAULT '{}'::jsonb,
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb
);
CREATE TABLE public.uido_round_holes (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  round_id uuid NOT NULL REFERENCES public.uido_rounds(id),
  hole_id uuid REFERENCES public.course_holes(id),
  hole_number integer NOT NULL,
  score integer,
  putts integer,
  net_score integer,
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb
);
CREATE TABLE public.uido_shots (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL,
  round_id uuid REFERENCES public.uido_rounds(id),
  round_hole_id uuid REFERENCES public.uido_round_holes(id),
  shot_number integer NOT NULL,
  recorded_at timestamptz NOT NULL DEFAULT now(),
  location text,
  club_id uuid,
  lie text,
  wind_speed numeric,
  wind_direction_degrees numeric,
  trajectory text,
  shape text,
  outcome text,
  free_aim_selected boolean NOT NULL DEFAULT false,
  decision_note text,
  source_provider text,
  source_record_id text,
  raw_source_data jsonb NOT NULL DEFAULT '{}'::jsonb,
  uido_interpretation jsonb NOT NULL DEFAULT '{}'::jsonb,
  device_context jsonb NOT NULL DEFAULT '{}'::jsonb,
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb
);

ALTER TABLE public.courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.course_versions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.tee_sets ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.course_holes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.uido_rounds ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.uido_round_holes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.uido_shots ENABLE ROW LEVEL SECURITY;

CREATE POLICY courses_public_read ON public.courses
FOR SELECT TO anon, authenticated USING (status = 'active');
CREATE POLICY course_versions_public_read ON public.course_versions
FOR SELECT TO anon, authenticated USING (status = 'published');
CREATE POLICY tee_sets_public_read ON public.tee_sets
FOR SELECT TO anon, authenticated
USING (EXISTS (
  SELECT 1 FROM public.course_versions v
  WHERE v.id = tee_sets.course_version_id AND v.status = 'published'
));
CREATE POLICY course_holes_public_read ON public.course_holes
FOR SELECT TO anon, authenticated
USING (EXISTS (
  SELECT 1 FROM public.course_versions v
  WHERE v.id = course_holes.course_version_id AND v.status = 'published'
));

CREATE POLICY "Users can read their own rounds" ON public.uido_rounds
FOR SELECT TO authenticated USING ((SELECT auth.uid()) = user_id);
CREATE POLICY "Users can insert their own rounds" ON public.uido_rounds
FOR INSERT TO authenticated WITH CHECK ((SELECT auth.uid()) = user_id);
CREATE POLICY "Users can update their own rounds" ON public.uido_rounds
FOR UPDATE TO authenticated USING ((SELECT auth.uid()) = user_id)
WITH CHECK ((SELECT auth.uid()) = user_id);
CREATE POLICY "Users can delete their own rounds" ON public.uido_rounds
FOR DELETE TO authenticated USING ((SELECT auth.uid()) = user_id);

CREATE POLICY "Users can read their own round holes" ON public.uido_round_holes
FOR SELECT TO authenticated USING (EXISTS (
  SELECT 1 FROM public.uido_rounds r
  WHERE r.id = uido_round_holes.round_id AND r.user_id = (SELECT auth.uid())
));
CREATE POLICY "Users can insert their own round holes" ON public.uido_round_holes
FOR INSERT TO authenticated WITH CHECK (EXISTS (
  SELECT 1 FROM public.uido_rounds r
  WHERE r.id = uido_round_holes.round_id AND r.user_id = (SELECT auth.uid())
));
CREATE POLICY "Users can update their own round holes" ON public.uido_round_holes
FOR UPDATE TO authenticated USING (EXISTS (
  SELECT 1 FROM public.uido_rounds r
  WHERE r.id = uido_round_holes.round_id AND r.user_id = (SELECT auth.uid())
)) WITH CHECK (EXISTS (
  SELECT 1 FROM public.uido_rounds r
  WHERE r.id = uido_round_holes.round_id AND r.user_id = (SELECT auth.uid())
));
CREATE POLICY "Users can delete their own round holes" ON public.uido_round_holes
FOR DELETE TO authenticated USING (EXISTS (
  SELECT 1 FROM public.uido_rounds r
  WHERE r.id = uido_round_holes.round_id AND r.user_id = (SELECT auth.uid())
));

CREATE POLICY "Users can read their own shots" ON public.uido_shots
FOR SELECT TO authenticated USING ((SELECT auth.uid()) = user_id);
CREATE POLICY "Users can insert their own shots" ON public.uido_shots
FOR INSERT TO authenticated WITH CHECK ((SELECT auth.uid()) = user_id);
CREATE POLICY "Users can update their own shots" ON public.uido_shots
FOR UPDATE TO authenticated USING ((SELECT auth.uid()) = user_id)
WITH CHECK ((SELECT auth.uid()) = user_id);
CREATE POLICY "Users can delete their own shots" ON public.uido_shots
FOR DELETE TO authenticated USING ((SELECT auth.uid()) = user_id);

GRANT SELECT ON public.courses, public.course_versions, public.tee_sets, public.course_holes TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.uido_rounds, public.uido_round_holes, public.uido_shots TO authenticated;

-- Fixed fixtures: active course A, closed course B; one published and one draft version.
INSERT INTO public.courses (id, status) VALUES
('10000000-0000-4000-8000-000000000001', 'active'),
('10000000-0000-4000-8000-000000000002', 'closed');
INSERT INTO public.course_versions (id, course_id, status) VALUES
('20000000-0000-4000-8000-000000000001', '10000000-0000-4000-8000-000000000001', 'published'),
('20000000-0000-4000-8000-000000000002', '10000000-0000-4000-8000-000000000001', 'draft'),
('20000000-0000-4000-8000-000000000003', '10000000-0000-4000-8000-000000000002', 'published');
INSERT INTO public.tee_sets (id, course_version_id) VALUES
('30000000-0000-4000-8000-000000000001', '20000000-0000-4000-8000-000000000001'),
('30000000-0000-4000-8000-000000000002', '20000000-0000-4000-8000-000000000003');
INSERT INTO public.course_holes (id, course_version_id, hole_number) VALUES
('40000000-0000-4000-8000-000000000001', '20000000-0000-4000-8000-000000000001', 1),
('40000000-0000-4000-8000-000000000002', '20000000-0000-4000-8000-000000000003', 2),
('40000000-0000-4000-8000-000000000003', '20000000-0000-4000-8000-000000000001', 3);
INSERT INTO public.uido_rounds (id, user_id, course_id, course_version_id, status) VALUES
('50000000-0000-4000-8000-000000000001', '00000000-0000-4000-8000-000000000001', '10000000-0000-4000-8000-000000000001', '20000000-0000-4000-8000-000000000001', 'started'),
('50000000-0000-4000-8000-000000000002', '00000000-0000-4000-8000-000000000002', '10000000-0000-4000-8000-000000000001', '20000000-0000-4000-8000-000000000001', 'started');
INSERT INTO public.uido_round_holes (id, round_id, hole_id, hole_number) VALUES
('60000000-0000-4000-8000-000000000001', '50000000-0000-4000-8000-000000000001', '40000000-0000-4000-8000-000000000001', 1),
('60000000-0000-4000-8000-000000000002', '50000000-0000-4000-8000-000000000002', '40000000-0000-4000-8000-000000000001', 1),
('60000000-0000-4000-8000-000000000003', '50000000-0000-4000-8000-000000000001', '40000000-0000-4000-8000-000000000002', 2);
INSERT INTO public.uido_shots (id, user_id, round_id, round_hole_id, shot_number) VALUES
('70000000-0000-4000-8000-000000000001', '00000000-0000-4000-8000-000000000001', '50000000-0000-4000-8000-000000000001', '60000000-0000-4000-8000-000000000001', 1);
