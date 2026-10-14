DO $$
DECLARE
    listing_count bigint;
    located_count bigint;
    england_count bigint;
    scotland_count bigint;
    wales_count bigint;
    ni_count bigint;
BEGIN
    SELECT count(*) INTO listing_count FROM public.course_clubs;
    SELECT count(*) INTO located_count FROM public.course_clubs WHERE latitude IS NOT NULL AND longitude IS NOT NULL;
    SELECT count(*) INTO england_count FROM public.course_clubs WHERE country = 'England';
    SELECT count(*) INTO scotland_count FROM public.course_clubs WHERE country = 'Scotland';
    SELECT count(*) INTO wales_count FROM public.course_clubs WHERE country = 'Wales';
    SELECT count(*) INTO ni_count FROM public.course_clubs WHERE country = 'Northern Ireland';

    IF listing_count <> 4 THEN RAISE EXCEPTION 'Expected 4 fixture club rows, got %', listing_count; END IF;
    IF located_count <> 3 THEN RAISE EXCEPTION 'Expected 3 fixture centroids, got %', located_count; END IF;
    IF england_count <> 1 OR scotland_count <> 1 OR wales_count <> 1 OR ni_count <> 1 THEN
        RAISE EXCEPTION 'Country counts do not match source: %, %, %, %', england_count, scotland_count, wales_count, ni_count;
    END IF;
END
$$;

SET ROLE anon;
DO $$
DECLARE
    directory_count bigint;
    link_count bigint;
BEGIN
    SELECT count(*) INTO directory_count FROM public.course_clubs;
    SELECT count(*) INTO link_count FROM public.course_club_courses;
    IF directory_count <> 4 THEN RAISE EXCEPTION 'Anonymous directory read returned % rows', directory_count; END IF;
    IF link_count <> 1 THEN RAISE EXCEPTION 'Anonymous reader should see only the confirmed link, got %', link_count; END IF;
END
$$;
RESET ROLE;

DO $$
BEGIN
    IF NOT (SELECT relrowsecurity FROM pg_class WHERE oid = 'public.course_clubs'::regclass) THEN
        RAISE EXCEPTION 'RLS is disabled on course_clubs';
    END IF;
    IF NOT (SELECT relrowsecurity FROM pg_class WHERE oid = 'public.course_club_courses'::regclass) THEN
        RAISE EXCEPTION 'RLS is disabled on course_club_courses';
    END IF;
END
$$;
