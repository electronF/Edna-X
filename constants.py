import os

DATABASE_NAME = "database.sqlite"

WEB_API_PATH = os.path.join('webapi')

AI_MODEL_PATH = os.path.join('aimodel')

GENERATED_RESPONSE_MAX_LENGTH = 1000

PALM2_API_KEY_PATH = os.path.join('api_key.json')

PALM2_API_URL = "https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText?key={}"