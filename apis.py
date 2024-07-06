from fastapi import APIRouter, HTTPException
from dependency import dependency_loader
from Models import QueryModel

router = APIRouter()

dependencies = dependency_loader()

@router.get("/")
def getGreetingMessage():
    try:
        return {"result":"hehe"}
    except Exception as E:
        raise HTTPException(status_code=500, detail=str(E))
    
@router.post("/get-query-result")
def getQueryResult(query_request: QueryModel):
    try:
        return {"result":query_request.query}
    except Exception as E:
        raise HTTPException(status_code=500, detail=str(E))