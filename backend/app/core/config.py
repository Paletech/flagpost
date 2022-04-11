from environs import Env

env = Env()
env.read_env()

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', '')

PYTHONPATH = env('PYTHONPATH', '')
DATABASE_URL = env('DATABASE_URL', '')

PROJECT_NAME = "fastapi-admin"

SQLALCHEMY_DATABASE_URI = env('DATABASE_URL', '')

API_V1_STR = "/api/v1"
