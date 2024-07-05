from fastapi import FastAPI, HTTPException
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from dependency import dependency_loader
from Models import QueryModel

# Load Dependencies
dependencies = dependency_loader()

server = FastAPI()

@server.get("/")
def getGreetingMessage():
    try:
        return {"result":"hehe"}
    except Exception as E:
        raise HTTPException(status_code=500, detail=str(E))

@server.post("/get-query-result")
def getQueryResult(query_request: QueryModel):
    try:
        return {"result":query_request.query}
    except Exception as E:
        raise HTTPException(status_code=500, detail=str(E))
    
if __name__=="__main__":
    import uvicorn
    uvicorn.run(server, host="localhost", port=5000)