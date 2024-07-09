from fastapi import APIRouter, HTTPException
from dependency import dependency_loader
from Models import QueryModel
from query_handlers import get_relevant_links

router = APIRouter()

dependencies = dependency_loader()

# Constants
MAX_LINKS_ON_RESPONSE = 5

@router.get("/")
def getGreetingMessage(name: str):
    try:
        return {"response":f"Hi {name}, How may I help you today!"}
    except Exception as E:
        raise HTTPException(status_code=500, detail=str(E))
    
@router.post("/get-query-result")
def getQueryResult(query_request: QueryModel):
    try:
        relevant_links = get_relevant_links(
            dependencies["NLP"],
            query_request.query,
            dependencies["VECTORIZER"],
            dependencies["VECTORS"],
            dependencies["LINKS"],
            dependencies["NORMALIZER"],
            MAX_LINKS_ON_RESPONSE
        )
        response_message = f"Here are the top resources that I found on {query_request.query}:"
        return {"response_message": response_message,
                "relevant_links": relevant_links}
    except Exception as E:
        raise HTTPException(status_code=500, detail=str(E))