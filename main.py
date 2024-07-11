from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import apis
import uvicorn

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://nisarg851.github.io/HumberChatbot/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(apis.router)

uvicorn.run(app, host="localhost", port=5000)