/*
 1. FILE PURPOSE: Configured Axios instance for all backend calls.
 2. RESPONSIBILITIES:
    - Set baseURL from NEXT_PUBLIC_API_URL; default headers; error interceptor.
 3. PLANNED CONTENTS: `export const api = axios.create({ baseURL })`.
 4. INPUTS / OUTPUTS: Inputs: env base URL. Outputs: a shared axios client.
 5. DEPENDS ON / USED BY: axios; used by lib/api/ingestion|training|evaluation.
*/
