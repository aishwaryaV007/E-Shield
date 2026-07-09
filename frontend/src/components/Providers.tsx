/*
 1. FILE PURPOSE: Client-side providers wrapper (TanStack Query).
 2. RESPONSIBILITIES:
    - Create a QueryClient and wrap children in QueryClientProvider.
    - Mount React Query Devtools in development.
 3. PLANNED CONTENTS: 'use client' Providers({ children }) component.
 4. INPUTS / OUTPUTS: Inputs: children. Outputs: context-wrapped tree.
 5. DEPENDS ON / USED BY: @tanstack/react-query; mounted in app/layout.tsx.
*/
