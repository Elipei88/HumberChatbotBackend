from fastapi import APIRouter, HTTPException
from model_binaries_controllers import model_binaries_loader, update_model_binaries_from_document
from Models import QueryModel
from preprocessing_controllers import preprocess_document
from query_controllers import get_relevant_links
from web_scrapper_controllers import web_scrapper

router = APIRouter()

model_binaries = model_binaries_loader()

# Constants
MAX_LINKS_ON_RESPONSE = 25
THRESHOLD = 0.1

def generate_cosine_similarity_graph(query: str, top_n: int = 5):
    """
    This function takes a query, processes it, computes cosine similarities with the documents,
    prints the top documents, and generates a cosine similarity bar graph.
    """
    # Extract needed components from model_binaries
    nlp = model_binaries["NLP"]
    vectorizer = model_binaries["VECTORIZER"]
    vectors = model_binaries["VECTORS"]
    links = model_binaries["LINKS"]

    # Process the query using the existing query processing function
    # Note: The code in query_controllers.get_relevant_links also processes queries,
    # but we will directly use the lower-level process_query function here.
    processed_query = process_query(query, nlp)
    
    # Convert processed query into a vector
    query_vector = vectorizer.transform([processed_query])

    # Compute cosine similarities (returns an Nx1 array)
    cosines = get_cosine_similarities(vectors, query_vector).flatten()

    # Zip links with their similarity scores
    doc_scores = list(zip(links, cosines))
    # Sort by score descending
    doc_scores.sort(key=lambda x: x[1], reverse=True)

    # Print top results
    print(f"\nTop {top_n} Documents for the Query: \"{query}\"")
    for doc, score in doc_scores[:top_n]:
        print(f"Document: {doc}, Similarity: {score}")

    # Plotting the top_n results in a horizontal bar chart
    top_docs = doc_scores[:top_n]
    doc_titles = [d for d, s in top_docs]
    similarity_scores = [s for d, s in top_docs]

    plt.figure(figsize=(10, 6))
    plt.barh(doc_titles, similarity_scores, color='skyblue')
    plt.xlabel("Cosine Similarity")
    plt.ylabel("Documents")
    plt.title(f"Cosine Similarities for Query: '{query}'")
    plt.xlim(0, 1)  # similarity scores are generally between 0 and 1
    plt.tight_layout()

    # Save the plot to a file
    plt.savefig("cosine_similarity_plot.png", bbox_inches="tight")
    plt.close()  # close the figure to free memory
    
    print("Cosine similarity plot saved as 'cosine_similarity_plot.png' in the current directory.")



@router.post("/get-query-result")
def getQueryResult(query_request: QueryModel):
    try:
        status, relevant_links = get_relevant_links(
            nlp=model_binaries["NLP"],
            query=query_request.query,
            vectorizer=model_binaries["VECTORIZER"],
            vectors=model_binaries["VECTORS"],
            links=model_binaries["LINKS"],
            n=MAX_LINKS_ON_RESPONSE,
            thres=THRESHOLD,
            usr=query_request.user_role
        )

        response_message = f"Here are the top resources that I found on {query_request.query}:"

        if status == -1:
            response_message = f"Unfortunatly, I was not able to find any resources relevant to \"{query_request.query}\". Please, Try again with any relevant keywords you can think of. You can also refer the main careers site:"

        return {"response_message": response_message,
                "relevant_links": relevant_links}
    except Exception as E:
        raise HTTPException(status_code=500, detail=str(E))
    
@router.post("/update-model")
def updateBinaries(token: str):
    url_to_document = web_scrapper(root="http://careers.humber.ca")
    url_to_document = preprocess_document(url_to_document)
    update_model_binaries_from_document(url_to_document)
    return {"message":"Model's Binaries are updated successfully"}
