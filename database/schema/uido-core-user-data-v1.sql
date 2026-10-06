-- UiDo Core User Data — live schema baseline
-- Applied directly to Supabase project uido-production on 2026-10-06.
-- This is a source-of-truth schema snapshot, not a Supabase migration file.

alter table public.uido_profiles
  add column if not exists home_course_id uuid references public.courses(id),
  add column if not exists status text not null default 'active'
    check (status in ('active','retired','anonymized')),
  add column if not exists retired_at timestamptz,
  add column if not exists anonymized_at timestamptz,
  add column if not exists metadata jsonb not null default '{}'::jsonb;

create table public.uido_user_preferences (...);
create table public.uido_handicap_records (...);
create table public.uido_equipment (...);
create table public.uido_clubs (...);
create table public.uido_rounds (...);
create table public.uido_round_holes (...);
create table public.uido_shots (...);
create table public.uido_external_records (...);

-- All eight new tables have RLS enabled.
-- Owner policies restrict customer data to auth.uid().
-- See live Supabase schema for the complete column definitions and policies.
