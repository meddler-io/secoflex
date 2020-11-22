import os

from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings, Secret
from databases import DatabaseURL

API_V1_STR = "/api"

JWT_TOKEN_PREFIX = "Token"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # one week

load_dotenv(".env")

MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))
SECRET_KEY = Secret(os.getenv("SECRET_KEY", "secret key for project"))

PROJECT_NAME = os.getenv("PROJECT_NAME", "FastAPI example application")
ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", ""))

MONGODB_URL = os.getenv("MONGODB_URL", "")  # deploying without docker-compose
FILESTORAGE_PATH = os.getenv("FILESTORAGE_PATH", "/tmp/")  # deploying without docker-compose

if not MONGODB_URL:
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
    MONGO_USER = os.getenv("MONGO_USER", "admin")
    MONGO_PASS = os.getenv("MONGO_PASSWORD", "markqiu")
    MONGO_DB = os.getenv("MONGO_DB", "fastapi")
    MONGO_AUTH = os.getenv("MONGO_AUTH", True)

    if MONGO_AUTH == True:
        MONGODB_URL = DatabaseURL(
            f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
        )
    else:
        MONGODB_URL = DatabaseURL(
            f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
        )
        
else:
    MONGODB_URL = DatabaseURL(MONGODB_URL)

database_name = MONGO_DB
article_collection_name = "articles"
favorites_collection_name = "favorites"
tags_collection_name = "tags"
users_collection_name = "users"
comments_collection_name = "commentaries"
followers_collection_name = "followers"
files_collection_name = "files"

form_field_group_schema_collection_name = "form_field_group_schema"
form_field_schema_collection_name = "form_field_schema"
form_report_schema_collection_name = "form_report_schema"
forms_schema_collection_name = "form_schema"
form_template_collection_name = "form_template"


asset_host_collection_name = "asset_host"
asset_domain_collection_name = "asset_domain"
asset_android_collection_name = "asset_android"
asset_ios_collection_name = "asset_ios"
asset_web_collection_name = "asset_web"
asset_repository_collection_name = "asset_repository"
asset_docker_collection_name = "asset_docker"




