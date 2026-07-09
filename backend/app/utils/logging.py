# 1. FILE PURPOSE: Centralised logger configuration.
# 2. RESPONSIBILITIES:
#    - Configure log format and level from settings (LOG_LEVEL).
#    - Provide get_logger(name) for modules.
# 3. PLANNED CONTENTS: setup_logging(level); get_logger(name) -> logging.Logger.
# 4. INPUTS / OUTPUTS: Inputs: LOG_LEVEL. Outputs: configured Logger instances.
# 5. DEPENDS ON / USED BY: logging, config.py; used across the backend.
