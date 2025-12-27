import os
from pathlib import Path

# Database configuration
DB_PATH = os.getenv("DB_PATH", "data/context.db")

# Ensure db directory exists
Path(DB_PATH).parent.mkdir(exist_ok=True)

# Noopur integration
NOOPUR_BASE_URL = os.getenv("NOOPUR_BASE_URL", "http://localhost:5001")
# Toggle remote integration; set to "1" or "true" to enable
INTEGRATOR_USE_NOOPUR = os.getenv("INTEGRATOR_USE_NOOPUR", "false").lower() in ("1", "true", "yes")
NOOPUR_API_KEY = os.getenv("NOOPUR_API_KEY", "")
# SSPL config
# Allowed clock drift (seconds) for timestamps
SSPL_ALLOW_DRIFT_SECONDS = int(os.getenv("SSPL_ALLOW_DRIFT_SECONDS", "300"))

# MongoDB configuration
MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING", "mongodb://localhost:27017")
MONGODB_DATABASE_NAME = os.getenv("MONGODB_DATABASE_NAME", "core_integrator")
USE_MONGODB = os.getenv("USE_MONGODB", "false").lower() in ("1", "true", "yes")