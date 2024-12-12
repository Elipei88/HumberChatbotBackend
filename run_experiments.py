import os
import re
import numpy as np
import matplotlib.pyplot as plt
import csv
from backend.model_binaries_controllers import model_binaries_loader
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import ttest_rel

# Load model binaries
model_binaries = model_binaries_loader()
vectorizer = model_binaries["VECTORIZER"]
vectors = model_binaries["VECTORS"]
links = model_binaries["LINKS"]

def retrieve_top_docs(query, top_n=5):
    """
    Retrieve top N documents for a given query using TF-IDF vectors and cosine similarity.
    """
    # Transform the query using the loaded vectorizer
    query_vector = vectorizer.transform([query])
    # Compute cosine similarities between the query and all document vectors
    sims = cosine_similarity(vectors, query_vector).flatten()
    # Combine links with similarities
    doc_scores = list(zip(links, sims))
    # Sort by similarity descending
    doc_scores.sort(key=lambda x: x[1], reverse=True)
    # Return top N documents
    return doc_scores[:top_n]

def extract_domain_terms(top_docs):
    """
    Extract domain-related terms from the top documents by simple regex patterns on their URLs.
    """
    domain_terms = set()
    for doc_url, _ in top_docs:
        # Extract the base filename from the URL
        filename = doc_url.split('/')[-1]
        base = filename.replace('.php', '')
        # Extract domain terms using regex patterns
        match = re.findall(r'(resources-online-learning|student-online-services|career-advising)', base)
        domain_terms.update(match)
    return list(domain_terms)

def refine_query(base_query, domain_terms):
    """
    Refine the query by adding domain terms and a known educational descriptor phrase.
    """
    descriptor = "online resume and interview improvement tools"
    # Add up to two domain terms for relevance
    domain_part = " ".join(domain_terms[:2])
    refined_query = f"{base_query} {domain_part} {descriptor}"
    return refined_query.strip()

# Baseline queries
baseline_queries = [
    "How can I prepare for an interview?",
    "What resources does Humber offer for interview practice?",
    "Tips to improve my interview skills at Humber College",
    "Online career coaching sessions focused on interview techniques accessible through Humber’s resources-online-learning and student-online-services platforms",
    "Detailed resume and interview preparation toolkit integrated with Humber’s student-online-services and resources-online-learning"
]

baseline_scores = []
refined_scores = []
improved_queries = []

# List to store all queries and their results for CSV
results = []

for q in baseline_queries:
    # Baseline retrieval
    top_docs_base = retrieve_top_docs(q)
    base_top_sim = top_docs_base[0][1] if top_docs_base else 0.0
    baseline_scores.append(base_top_sim)
    
    # Extract domain terms from top documents
    domain_terms = extract_domain_terms(top_docs_base)
    
    # Refine query
    refined_query = refine_query(q, domain_terms)
    
    # Retrieve with refined query
    top_docs_refined = retrieve_top_docs(refined_query)
    ref_top_sim = top_docs_refined[0][1] if top_docs_refined else 0.0
    refined_scores.append(ref_top_sim)
    
    # Append to results list
    results.append([q, base_top_sim, ref_top_sim])

# Save results to CSV
with open("results.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Query", "Baseline_TopSim", "Refined_TopSim"])
    writer.writerows(results)

# Perform paired t-test
t_stat, p_value = ttest_rel(baseline_scores, refined_scores)

# Print t-test results
print(f"Paired t-test results:\nT-statistic: {t_stat:.4f}, P-value: {p_value:.4f}")

# Save t-test results to CSV
with open("ttest_results.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["T-statistic", "P-value"])
    writer.writerow([f"{t_stat:.4f}", f"{p_value:.4f}"])

# Generate comparison plot
x = np.arange(len(baseline_queries))
width = 0.35
fig, ax = plt.subplots(figsize=(12,6))
bars1 = ax.bar(x - width/2, baseline_scores, width, label='Baseline', color='lightgray')
bars2 = ax.bar(x + width/2, refined_scores, width, label='Refined', color='skyblue')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Top Similarity')
ax.set_title('Baseline vs. Refined Query Similarities for Five Queries')
ax.set_xticks(x)
ax.set_xticklabels([f"Q{i+1}" for i in range(len(baseline_queries))], rotation=45, ha='right')
ax.legend()

# Attach a text label above each bar, displaying its height
def autolabel(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(bars1)
autolabel(bars2)

fig.tight_layout()
plt.savefig("comparison_plot.png")
plt.close()

print("Done. results.csv, ttest_results.csv, and comparison_plot.png have been generated.")
