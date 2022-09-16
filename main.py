from fastapi import FastAPI

#Project
from api import router
from starlette.middleware.cors import CORSMiddleware
from database import Base, engine
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], expose_headers=["*"])

Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/api/v1")