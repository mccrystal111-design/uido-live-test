-- UiDo user security hardening
-- Applied to Supabase project uido-production (itmlfcaukkngcoxaxcgm)
--
-- User profile data is owner-only. Passwords remain in Supabase Auth;
-- public application tables never store password material.
--
-- The trigger function is database-internal and must not be callable through
-- the PostgREST RPC surface.
--
-- PostGIS st_estimatedextent functions are vendor-managed SECURITY DEFINER
-- functions; their public execution grants are handled separately by the
-- Supabase/PostGIS installation and are not modified here.

ALTER TABLE public.uido_profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read their own UiDo profile"
ON public.uido_profiles
FOR SELECT
TO authenticated
USING ((SELECT auth.uid()) = id);

CREATE POLICY "Users can insert their own UiDo profile"
ON public.uido_profiles
FOR INSERT
TO authenticated
WITH CHECK ((SELECT auth.uid()) = id);

CREATE POLICY "Users can update their own UiDo profile"
ON public.uido_profiles
FOR UPDATE
TO authenticated
USING ((SELECT auth.uid()) = id)
WITH CHECK ((SELECT auth.uid()) = id);

REVOKE EXECUTE ON FUNCTION public.handle_new_user() FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION public.handle_new_user() FROM anon;
REVOKE EXECUTE ON FUNCTION public.handle_new_user() FROM authenticated;
