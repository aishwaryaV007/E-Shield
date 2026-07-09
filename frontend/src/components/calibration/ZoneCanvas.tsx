/*
 1. FILE PURPOSE: Interactive canvas to draw calibration zones over a sheet image.
 2. RESPONSIBILITIES:
    - Render the sample page and let the user draw/resize rectangles (react-konva).
    - Emit zone bboxes (marks/total/roll-no/answer) as template JSON.
 3. PLANNED CONTENTS: ZoneCanvas({ image, onChange }) with Konva Stage/Layer/Rect.
 4. INPUTS / OUTPUTS: Inputs: page image + existing zones. Outputs: onChange(zones) callback.
 5. DEPENDS ON / USED BY: react-konva/konva; used by app/calibration/page.tsx.
*/
