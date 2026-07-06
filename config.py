from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG={
    "user":os.getenv("DB_USER"),
    "password":os.getenv("DB_PASSWORD"),
    "host":os.getenv("DB_HOST"),
    "database":os.getenv("DB_NAME"),
    "port":int(os.getenv("DB_PORT"))
}