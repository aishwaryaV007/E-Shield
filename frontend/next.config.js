/*
 1. FILE PURPOSE: Next.js configuration, including API rewrites/proxy to the FastAPI backend.
 2. RESPONSIBILITIES:
    - Define rewrites so /api/* proxies to NEXT_PUBLIC_API_URL (avoids CORS in dev).
    - Set React strict mode and build options.
 3. PLANNED CONTENTS: module.exports nextConfig with async rewrites().
 4. INPUTS / OUTPUTS: Inputs: env NEXT_PUBLIC_API_URL. Outputs: Next.js build/runtime config.
 5. DEPENDS ON / USED BY: Next.js build; pairs with lib/api/client.ts base URL.
*/
