from fastapi import APIRouter, HTTPException
from dependency import dependency_loader
from Models import QueryModel
from query_handlers import get_relevant_links
from query_handlers import web_scrapper

router = APIRouter()

dependencies = dependency_loader()

# Constants
MAX_LINKS_ON_RESPONSE = 25
THRESHOLD = 0.1
    
@router.post("/get-query-result")
def getQueryResult(query_request: QueryModel):
    try:
        status, relevant_links = get_relevant_links(
            dependencies["NLP"],
            query_request.query,
            dependencies["VECTORIZER"],
            dependencies["VECTORS"],
            dependencies["LINKS"],
            MAX_LINKS_ON_RESPONSE,
            THRESHOLD
        )

        response_message = f"Here are the top resources that I found on {query_request.query}:"

        if status == -1:
            response_message = f"Unfortunatly, I was not able to find any resources relevant to \"{query_request.query}\". Please, Try again with any relevant keywords you can think of. You can also refer the main careers site:"

        return {"response_message": response_message,
                "relevant_links": relevant_links}
    except Exception as E:
        raise HTTPException(status_code=500, detail=str(E))
    
@router.post("/update-vectors")
def updateVectors(token: str):
    web_scrapper(root="http://careers.humber.ca")
    return {"message":"The Vectors are updated successfully"}