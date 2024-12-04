import os


class Config:
    SECRET_KEY = os.environ.get("SECRET") or "hard to guess string"
