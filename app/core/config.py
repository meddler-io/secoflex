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

# MessageQ Topics
MQ_TOOLBUILDER_QUEUE = os.getenv("MQ_TOOLBUILDER_QUEUE", "MQ_TOOLBUILDER_QUEUE")  # deploying without docker-compose


MONGODB_URL = os.getenv("MONGODB_URL", "")  # deploying without docker-compose
FILESTORAGE_PATH = os.getenv("FILESTORAGE_PATH", "/tmp/")  # deploying without docker-compose
MINIO_URL = os.getenv("MINIO_URL", "192.168.29.5:9000")  # deploying without docker-compose
MINIO_ACCESSKEY = os.getenv("MINIO_ACCESSKEY", "MEDDLER")  # deploying without docker-compose
MINIO_SECRET = os.getenv("MINIO_SECRET", "SUPERDUPERSECRET")  # deploying without docker-compose
MINIO_REGION = os.getenv("MINIO_REGION", "meddler")  # deploying without docker-compose


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


# Tools
tools_collection_name = "tools"
build_collection_name = "builds"
build_executor_collection_name = "builds_executor"
job_collection_name = "jobs"


# Webhooks
API_PREFIX_WEBHOOK = "http://192.168.29.10:8000/api/v2"
SUCCESS_EXECUTION_WEBHOOK = f"{API_PREFIX_WEBHOOK}/result/success/%s"
FAILURE_EXECUTION_WEBHOOK = f"{API_PREFIX_WEBHOOK}/result/failure/%s"

# Job Webhhoks
JOB_SUCCESS_EXECUTION_WEBHOOK = f"{API_PREFIX_WEBHOOK}/job/result/success/%s"
JOB_FAILURE_EXECUTION_WEBHOOK = f"{API_PREFIX_WEBHOOK}/job/result/failure/%s"

# Provider
NOMAD_API_ENDPOINT = "http://192.168.29.5:4646/v1"
NOMAD_API_JOBS = f"{NOMAD_API_ENDPOINT}/jobs"
NOMAD_API_JOB = f"{NOMAD_API_ENDPOINT}/job"
NOMAD_API_GC = f"{NOMAD_API_ENDPOINT}/system/gc"
NOMAD_API_SEARCH = f"{NOMAD_API_ENDPOINT}/search"
# DOCKER BASE URL
DOCKER_ENDPOINT = "192.168.29.5:5000"
DOCKER_API_CATALOG = f"http://{DOCKER_ENDPOINT}/v2/_catalog"

# 
DOCKER_DEFAULT_NAMESPACE = "rounak316"
# Docker Private Registry
DOCKER_PRIVATE_REGISTRY = "192.168.29.5:5000/{}:{}"

