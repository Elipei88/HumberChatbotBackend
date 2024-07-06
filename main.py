from fastapi import FastAPI
import apis
import uvicorn

app = FastAPI()
app.include_router(apis.router)

uvicorn.run(app, host="localhost", port=5000)