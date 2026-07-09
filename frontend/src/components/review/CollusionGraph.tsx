/*
 1. FILE PURPOSE: Renders the CopyCatch collusion graph from backend JSON using react-force-graph; nodes = scripts, edges = suspicious pairs.
 2. RESPONSIBILITIES:
    - Fetch graph JSON from API.
    - Render interactive PyVis-style force graph.
    - Handle node click events to open side-by-side evidence.
 3. PLANNED CONTENTS: CollusionGraph React component. Takes JSON graph data. Returns ForceGraph2D/3D JSX.
 4. INPUTS / OUTPUTS: Inputs: CopyCatch graph JSON. Outputs: Interactive React component.
 5. DEPENDS ON / USED BY: react-force-graph, vis-network, backend API.
*/
