-- UiDo Core User Data — schema baseline
-- Live Supabase application schema applied 2026-10-06.
-- This is a Git-backed schema snapshot; Supabase migration history remains separate.

alter table public.uido_profiles
  add column if not exists home_course_id uuid references public.courses(id),
  add column if not exists status text not null default 'active' check (status in ('active','retired','anonymized')),
  add column if not exists retired_at timestamptz,
  add column if not exists anonymized_at timestamptz,
  add column if not exists metadata jsonb not null default '{}'::jsonb;

create table if not exists public.uido_user_preferences (
  user_id uuid primary key references auth.users(id) on delete cascade,
  distance_unit text not null default 'yards' check (distance_unit in ('yards','metres')),
  default_tee_set_id uuid references public.tee_sets(id),
  notifications_enabled boolean not null default true,
  preferences jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

create table if not exists public.uido_handicap_records (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  provider text not null check (provider in ('uido','whs','ghin','other')),
  handicap_type text not null check (handicap_type in ('official','practice','other')),
  handicap_index numeric,
  effective_at timestamptz not null default now(),
  external_id text,
  source_metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.uido_equipment (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  category text not null,
  manufacturer text,
  model text,
  name text,
  handedness text,
  valid_from timestamptz not null default now(),
  valid_to timestamptz,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.uido_clubs (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  equipment_id uuid references public.uido_equipment(id) on delete set null,
  club_name text not null,
  club_category text,
  carry_distance numeric,
  carry_distance_unit text not null default 'yards' check (carry_distance_unit in ('yards','metres')),
  valid_from timestamptz not null default now(),
  valid_to timestamptz,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.uido_rounds (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  course_id uuid not null references public.courses(id),
  course_version_id uuid not null references public.course_versions(id),
  tee_set_id uuid references public.tee_sets(id),
  round_type text not null default 'scored' check (round_type in ('scored','practice','practice_session')),
  status text not null default 'completed' check (status in ('started','completed','abandoned')),
  started_at timestamptz not null default now(),
  ended_at timestamptz,
  start_location geometry(Point,4326),
  course_selection_method text check (course_selection_method in ('gps_nearest','manual','offline','other')),
  device_context jsonb not null default '{}'::jsonb,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  check (ended_at is null or ended_at >= started_at)
);

create table if not exists public.uido_round_holes (
  id uuid primary key default gen_random_uuid(),
  round_id uuid not null references public.uido_rounds(id) on delete cascade,
  hole_id uuid references public.course_holes(id),
  hole_number integer not null check (hole_number between 1 and 99),
  score integer,
  putts integer check (putts is null or putts >= 0),
  net_score integer,
  metadata jsonb not null default '{}'::jsonb,
  unique(round_id, hole_number)
);

create table if not exists public.uido_shots (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  round_id uuid references public.uido_rounds(id) on delete cascade,
  round_hole_id uuid references public.uido_round_holes(id) on delete cascade,
  shot_number integer not null check (shot_number > 0),
  recorded_at timestamptz not null default now(),
  location geometry(Point,4326),
  club_id uuid references public.uido_clubs(id) on delete set null,
  lie text,
  wind_speed numeric,
  wind_direction_degrees numeric,
  trajectory text,
  shape text,
  outcome text,
  free_aim_selected boolean not null default false,
  decision_note text,
  source_provider text,
  source_record_id text,
  raw_source_data jsonb not null default '{}'::jsonb,
  uido_interpretation jsonb not null default '{}'::jsonb,
  device_context jsonb not null default '{}'::jsonb,
  metadata jsonb not null default '{}'::jsonb,
  unique(round_hole_id, shot_number)
);

create table if not exists public.uido_external_records (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  provider text not null,
  record_type text not null,
  external_id text,
  observed_at timestamptz,
  received_at timestamptz not null default now(),
  round_id uuid references public.uido_rounds(id) on delete set null,
  raw_payload jsonb not null,
  interpretation jsonb not null default '{}'::jsonb,
  metadata jsonb not null default '{}'::jsonb,
  unique(user_id, provider, record_type, external_id)
);

-- RLS is enabled on all customer-owned tables.
-- Policies enforce auth.uid() ownership for direct customer data.
