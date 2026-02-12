import os

class Settings:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://Shubham:1234@cluster0.tzsdxh3.mongodb.net/")
    DB_NAME = os.getenv("DB_NAME", "agent_logs")
    API_KEY_HEADER = "x-api-key"

settings = Settings()
