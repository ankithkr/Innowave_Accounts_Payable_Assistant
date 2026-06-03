import os

from dotenv import load_dotenv

load_dotenv()

SERVICE_ACCOUNT_FILE = os.getenv(
    "GOOGLE_SERVICE_ACCOUNT_FILE"
)

GOOGLE_DRIVE_FOLDER_ID = os.getenv(
    "GOOGLE_DRIVE_FOLDER_ID"
)

# OAuth settings for Drive (optional)
OAUTH_CLIENT_SECRETS_FILE = os.getenv("OAUTH_CLIENT_SECRETS_FILE", "")
# Path to store OAuth token (will be created after user authorizes)
OAUTH_TOKEN_FILE = os.getenv("OAUTH_TOKEN_FILE", "backend/token_drive.json")
# Use OAuth for Drive API when set to true (1/true/yes)
_use_oauth = os.getenv("GOOGLE_USE_OAUTH", "").lower()
GOOGLE_USE_OAUTH = _use_oauth in ("1", "true", "yes")