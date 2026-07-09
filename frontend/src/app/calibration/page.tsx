/*
 1. FILE PURPOSE: Calibration page — draw a zone template on a sample sheet.
 2. RESPONSIBILITIES:
    - Host the ZoneCanvas for drawing marks/total/roll-no/answer rectangles.
    - Save the resulting template JSON via the calibration API.
 3. PLANNED CONTENTS: CalibrationPage() component wrapping ZoneCanvas + save controls.
 4. INPUTS / OUTPUTS: Inputs: sample page image + drawn zones. Outputs: saved template.
 5. DEPENDS ON / USED BY: components/calibration/ZoneCanvas, lib/api (templates).
*/
