import os

DATABASE_NAME = "database.sqlite"

WEB_API_PATH = os.path.join('webapi')

STATIC_PATH = os.path.join('frontend', 'static')

TEMPLATES_PATH = os.path.join('frontend', 'templates')

ABS_PATH = os.path.abspath(os.path.dirname(__file__))

UPLOADED_DOCUMENTS_PATH = os.path.join(ABS_PATH, WEB_API_PATH, 'uploaded', 'documents')

COVER_IMAGES_FOLDER = 'covers'

COVER_IMAGES_PATH = os.path.join(ABS_PATH, STATIC_PATH, COVER_IMAGES_FOLDER)