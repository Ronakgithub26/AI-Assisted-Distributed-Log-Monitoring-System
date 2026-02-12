from fastapi import FastAPI
from routes.collect import router as collect_router

app = FastAPI(title="Agent Log Collector")

app.include_router(collect_router, prefix="/api")

