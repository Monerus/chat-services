from fastapi import FastAPI
import uvicorn
from app.routes import router as messages_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(messages_router)

if __name__ == "__main__":
    uvicorn.run("main:app")