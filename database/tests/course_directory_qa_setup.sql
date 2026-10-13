DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'anon') THEN
        CREATE ROLE anon NOLOGIN;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'authenticated') THEN
        CREATE ROLE authenticated NOLOGIN;
    END IF;
END
$$;

CREATE TABLE public.courses (
    id uuid PRIMARY KEY,
    canonical_name text NOT NULL
);

INSERT INTO public.courses (id, canonical_name)
VALUES ('00000000-0000-4000-8000-000000000001', 'QA course');
