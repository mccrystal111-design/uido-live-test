-- Candidate schema for the public UK club directory.
-- Apply only through a reviewed Supabase migration after isolated QA.
-- Club listings are kept separate from geometry-bearing course records.

CREATE TABLE public.course_clubs (
    id uuid PRIMARY KEY,
    directory_key text NOT NULL UNIQUE,
    club_name text NOT NULL CHECK (length(trim(club_name)) > 0),
    country text NOT NULL,
    country_code text NOT NULL DEFAULT 'GB' CHECK (country_code = 'GB'),
    country_subdivision text,
    postal_address text NOT NULL,
    phone text,
    website text,
    email text,
    contact_name text,
    contact_title text,
    latitude double precision,
    longitude double precision,
    coordinate_status text NOT NULL CHECK (
        coordinate_status IN ('Postcode centroid', 'No postcode match', 'No postcode available')
    ),
    coordinate_source text NOT NULL,
    source_provider text NOT NULL,
    source_listing_url text NOT NULL UNIQUE,
    source_page_published text,
    source_file_sha256 text NOT NULL CHECK (source_file_sha256 ~ '^[0-9a-f]{64}$'),
    imported_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT course_clubs_latitude_range CHECK (latitude IS NULL OR latitude BETWEEN -90 AND 90),
    CONSTRAINT course_clubs_longitude_range CHECK (longitude IS NULL OR longitude BETWEEN -180 AND 180),
    CONSTRAINT course_clubs_coordinates_pair CHECK ((latitude IS NULL) = (longitude IS NULL)),
    CONSTRAINT course_clubs_coordinate_status_consistent CHECK (
        (coordinate_status = 'Postcode centroid' AND latitude IS NOT NULL AND longitude IS NOT NULL)
        OR (coordinate_status <> 'Postcode centroid' AND latitude IS NULL AND longitude IS NULL)
    )
);

CREATE INDEX course_clubs_country_name_idx ON public.course_clubs (country, lower(club_name));
CREATE INDEX course_clubs_location_idx ON public.course_clubs (latitude, longitude)
    WHERE latitude IS NOT NULL AND longitude IS NOT NULL;

CREATE TABLE public.course_club_courses (
    club_id uuid NOT NULL REFERENCES public.course_clubs(id) ON DELETE CASCADE,
    course_id uuid NOT NULL REFERENCES public.courses(id) ON DELETE CASCADE,
    match_status text NOT NULL CHECK (match_status IN ('suggested', 'confirmed', 'rejected')),
    match_method text NOT NULL,
    evidence jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    confirmed_at timestamptz,
    PRIMARY KEY (club_id, course_id),
    CONSTRAINT confirmed_link_requires_timestamp CHECK (match_status <> 'confirmed' OR confirmed_at IS NOT NULL)
);

CREATE INDEX course_club_courses_course_idx ON public.course_club_courses (course_id);

ALTER TABLE public.course_clubs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.course_club_courses ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS course_clubs_public_read ON public.course_clubs;
CREATE POLICY course_clubs_public_read
ON public.course_clubs
FOR SELECT
TO anon, authenticated
USING (true);

DROP POLICY IF EXISTS course_club_courses_confirmed_read ON public.course_club_courses;
CREATE POLICY course_club_courses_confirmed_read
ON public.course_club_courses
FOR SELECT
TO anon, authenticated
USING (match_status = 'confirmed');

GRANT SELECT ON public.course_clubs, public.course_club_courses TO anon, authenticated;
REVOKE INSERT, UPDATE, DELETE ON public.course_clubs, public.course_club_courses FROM anon, authenticated;
