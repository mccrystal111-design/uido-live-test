WITH course_club_payload(payload) AS (
    VALUES
        ('{"id":"00000000-0000-4000-8000-000000000101","directory_key":"fixture:england","club_name":"Fixture England Club","country":"England","country_code":"GB","country_subdivision":"ENG","postal_address":"Test address","location":{"type":"Point","coordinates":[-0.1,51.5]},"coordinate_status":"Postcode centroid","coordinate_source":"fixture","source_file_sha256":"0000000000000000000000000000000000000000000000000000000000000000","source":{"name":"Fixture","listing_url":"https://example.invalid/clubs/england"}}'::jsonb),
        ('{"id":"00000000-0000-4000-8000-000000000102","directory_key":"fixture:scotland","club_name":"Fixture Scotland Club","country":"Scotland","country_code":"GB","country_subdivision":"SCT","postal_address":"Test address","location":{"type":"Point","coordinates":[-3.2,55.9]},"coordinate_status":"Postcode centroid","coordinate_source":"fixture","source_file_sha256":"0000000000000000000000000000000000000000000000000000000000000000","source":{"name":"Fixture","listing_url":"https://example.invalid/clubs/scotland"}}'::jsonb),
        ('{"id":"00000000-0000-4000-8000-000000000103","directory_key":"fixture:wales","club_name":"Fixture Wales Club","country":"Wales","country_code":"GB","country_subdivision":"WLS","postal_address":"Test address","coordinate_status":"No postcode match","coordinate_source":"fixture","source_file_sha256":"0000000000000000000000000000000000000000000000000000000000000000","source":{"name":"Fixture","listing_url":"https://example.invalid/clubs/wales"}}'::jsonb),
        ('{"id":"00000000-0000-4000-8000-000000000104","directory_key":"fixture:northern-ireland","club_name":"Fixture Northern Ireland Club","country":"Northern Ireland","country_code":"GB","country_subdivision":"NIR","postal_address":"Test address","location":{"type":"Point","coordinates":[-5.9,54.6]},"coordinate_status":"Postcode centroid","coordinate_source":"fixture","source_file_sha256":"0000000000000000000000000000000000000000000000000000000000000000","source":{"name":"Fixture","listing_url":"https://example.invalid/clubs/northern-ireland"}}'::jsonb)
)

INSERT INTO public.course_clubs (
    id, directory_key, club_name, country, country_code, country_subdivision,
    postal_address, phone, website, email, contact_name, contact_title,
    latitude, longitude, coordinate_status, coordinate_source,
    source_provider, source_listing_url, source_page_published, source_file_sha256
)
SELECT
    (p.payload ->> 'id')::uuid,
    p.payload ->> 'directory_key',
    p.payload ->> 'club_name',
    p.payload ->> 'country',
    p.payload ->> 'country_code',
    p.payload ->> 'country_subdivision',
    p.payload ->> 'postal_address',
    p.payload ->> 'phone',
    p.payload ->> 'website',
    p.payload ->> 'email',
    p.payload ->> 'contact_name',
    p.payload ->> 'contact_title',
    CASE WHEN p.payload #>> '{location,coordinates,1}' IS NULL THEN NULL
        ELSE (p.payload #>> '{location,coordinates,1}')::double precision END,
    CASE WHEN p.payload #>> '{location,coordinates,0}' IS NULL THEN NULL
        ELSE (p.payload #>> '{location,coordinates,0}')::double precision END,
    p.payload ->> 'coordinate_status',
    p.payload ->> 'coordinate_source',
    p.payload #>> '{source,name}',
    p.payload #>> '{source,listing_url}',
    p.payload #>> '{source,page_published}',
    p.payload ->> 'source_file_sha256'
FROM course_club_payload AS p;

INSERT INTO public.course_club_courses (
    club_id, course_id, match_status, match_method, evidence, confirmed_at
)
SELECT id, '00000000-0000-4000-8000-000000000001', 'suggested', 'qa-fixture', '{}', NULL
FROM public.course_clubs
WHERE directory_key = (SELECT directory_key FROM public.course_clubs ORDER BY club_name LIMIT 1);

INSERT INTO public.course_club_courses (
    club_id, course_id, match_status, match_method, evidence, confirmed_at
)
SELECT id, '00000000-0000-4000-8000-000000000001', 'confirmed', 'qa-fixture', '{}', now()
FROM public.course_clubs
WHERE directory_key = (SELECT directory_key FROM public.course_clubs ORDER BY club_name OFFSET 1 LIMIT 1);
