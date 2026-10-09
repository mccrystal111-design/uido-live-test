-- UiDo Core round/shot persistence integrity hardening.
-- DRAFT ONLY: not applied to uido-production.
-- Apply and test in an isolated QA project before any production migration.
--
-- Guarantees:
--   * a new round can reference only an active course + published course version;
--   * a tee set, when supplied, belongs to that exact version;
--   * a round hole belongs to the user's round and, when hole_id is supplied,
--     to the same course version and hole number;
--   * a shot cannot attach another user's round/hole or mix round and hole IDs.

begin;

drop policy if exists "Users can insert their own rounds" on public.uido_rounds;
create policy "Users can insert their own rounds"
on public.uido_rounds
for insert
to authenticated
with check (
  (select auth.uid()) = user_id
  and exists (
    select 1
    from public.course_versions cv
    join public.courses c on c.id = cv.course_id
    where cv.id = uido_rounds.course_version_id
      and cv.course_id = uido_rounds.course_id
      and cv.status = 'published'
      and c.status = 'active'
  )
  and (
    tee_set_id is null
    or exists (
      select 1
      from public.tee_sets ts
      where ts.id = uido_rounds.tee_set_id
        and ts.course_version_id = uido_rounds.course_version_id
    )
  )
);

drop policy if exists "Users can insert their own round holes" on public.uido_round_holes;
create policy "Users can insert their own round holes"
on public.uido_round_holes
for insert
to authenticated
with check (
  exists (
    select 1
    from public.uido_rounds r
    where r.id = uido_round_holes.round_id
      and r.user_id = (select auth.uid())
      and (
        uido_round_holes.hole_id is null
        or exists (
          select 1
          from public.course_holes ch
          where ch.id = uido_round_holes.hole_id
            and ch.course_version_id = r.course_version_id
            and ch.hole_number = uido_round_holes.hole_number
        )
      )
  )
);

drop policy if exists "Users can insert their own shots" on public.uido_shots;
create policy "Users can insert their own shots"
on public.uido_shots
for insert
to authenticated
with check (
  (select auth.uid()) = user_id
  and (
    round_id is null
    or exists (
      select 1
      from public.uido_rounds r
      where r.id = uido_shots.round_id
        and r.user_id = (select auth.uid())
    )
  )
  and (
    round_hole_id is null
    or exists (
      select 1
      from public.uido_round_holes rh
      join public.uido_rounds r on r.id = rh.round_id
      where rh.id = uido_shots.round_hole_id
        and r.user_id = (select auth.uid())
    )
  )
  and (
    round_id is null
    or round_hole_id is null
    or exists (
      select 1
      from public.uido_round_holes rh
      where rh.id = uido_shots.round_hole_id
        and rh.round_id = uido_shots.round_id
    )
  )
);

drop policy if exists "Users can update their own shots" on public.uido_shots;
create policy "Users can update their own shots"
on public.uido_shots
for update
to authenticated
using ((select auth.uid()) = user_id)
with check (
  (select auth.uid()) = user_id
  and (
    round_id is null
    or exists (
      select 1
      from public.uido_rounds r
      where r.id = uido_shots.round_id
        and r.user_id = (select auth.uid())
    )
  )
  and (
    round_hole_id is null
    or exists (
      select 1
      from public.uido_round_holes rh
      join public.uido_rounds r on r.id = rh.round_id
      where rh.id = uido_shots.round_hole_id
        and r.user_id = (select auth.uid())
    )
  )
  and (
    round_id is null
    or round_hole_id is null
    or exists (
      select 1
      from public.uido_round_holes rh
      where rh.id = uido_shots.round_hole_id
        and rh.round_id = uido_shots.round_id
    )
  )
);

commit;
