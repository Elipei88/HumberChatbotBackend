import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def process_query(query, nlp):
    processed_query = ''
    for word in nlp(query):
        if word.text not in nlp.Defaults.stop_words:
            processed_query += ' ' + word.lemma_.lower()
    processed_query = processed_query.strip()
    return processed_query

def get_cosine_similarities(vectors, query_vector):
    cosine = cosine_similarity(vectors, query_vector)
    return cosine

def n_largest(cosines, n):
    n_largest_indexes = np.argpartition(cosines.flatten(), -n)[-n:]
    largest_index_magnitude_dict = {}
    
    for i in n_largest_indexes:
        if cosines.flatten()[i] not in largest_index_magnitude_dict.keys():
            largest_index_magnitude_dict[cosines.flatten()[i]] = [i]
        else:
            largest_index_magnitude_dict[cosines.flatten()[i]].append(i)
    
    sorted_magnitudes = sorted(largest_index_magnitude_dict.keys(), reverse=True)
    
    indexes = []
    for i in sorted_magnitudes:
        indexes += largest_index_magnitude_dict[i]
    
    return indexes

def get_n_largest_indexes(cosine, n):
    if cosine.max() > 0:
        return n_largest(cosine, n)
    else:
        return -1

def get_relevant_links(nlp, query, vectorizer, vectors, links, normalizer, n):
    processed_query = process_query(query, nlp)
    query_vector = vectorizer.transform([processed_query])
    query_vector = normalizer.transform(query_vector)
    cosines = get_cosine_similarities(vectors, query_vector)
    index = get_n_largest_indexes(cosines, n)
    if index == -1:
        return ['http://careers.humber.ca']
    return list(np.array(links)[index])