import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from dependency import dependency_file_path
import re

def get_links(doc_links):
    links = []
    for i in doc_links:
        link_list = i.split('[')[1].split(']')[0].split(',')
        min_len = len(link_list[0])
        min_lnk = link_list[0]
        for link in link_list:
            if len(link) < min_len:
                min_len = len(link)
                min_lnk = link
        links.append(min_lnk.strip().split("'")[1])
    return links

def process_to_vectorize_documents(all_docs, nlp):
    all_tokens = []
    for i in range(len(all_docs)):
        all_tokens.append(nlp(all_docs[i]))
    all_tkn_stp_wrds = []
    for doc in all_tokens:
        tokens = ''
        for token in doc:
            if token.text not in nlp.Defaults.stop_words:
                tokens += ' ' + token.lemma_.lower()
        all_tkn_stp_wrds.append(tokens.strip())
    return all_tkn_stp_wrds


def vectorize_all_docs(all_tkn_stp_wrds, vectorizer):
    vectorizer.fit(all_tkn_stp_wrds)
    vectors = vectorizer.transform(all_tkn_stp_wrds)
    return vectors

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

def n_largest(cosines, n, thres):
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
        if i > thres:
            indexes += largest_index_magnitude_dict[i]
    return indexes

def get_n_largest_indexes(cosine, n, thres):
    if cosine.max() > 0:
        indxs = n_largest(cosine, n, thres)
        if len(indxs) > 0:
            return indxs
        return -1
    else:
        return -1

def get_relevant_links(nlp, query, vectorizer, vectors, links, n, thres):
    lower_than_upper_split = re.sub(r"([a-z\.!?])([A-Z])", r"\1 \2", query)
    upper_than_lower_split = re.sub(r"([A-Z\.!?]{2,})([A-Z]{1}[a-z]{2,})", r"\1 \2", lower_than_upper_split)
    bracket_before = re.sub(r"([)])([A-Z])", r"\1 \2", upper_than_lower_split)
    bracket_after = re.sub(r"([a-z])([(])", r"\1 \2", bracket_before)
    rmv_smbl = re.sub(r'[^A-Za-z\n@]', ' ', bracket_after)
    rmv_spcs = re.sub(r'\s{2,}', ' ', rmv_smbl)
    processed_query = process_query(rmv_spcs, nlp)
    
    query_vector = vectorizer.transform([processed_query])
    cosines = get_cosine_similarities(vectors, query_vector)
    index = get_n_largest_indexes(cosines, n, thres)
    if index == -1:
        return (index, ['http://careers.humber.ca'])
    return (index, list(np.array(links)[index]))

def dump_file(filename, mode):
    with open(filename, mode) as fin:
        pickle.dump(filename, fin)

def update_vectors(file: str):
    doc_link = pd.read_excel('Doc_Link_complete_processed.xlsx')

    with open(dependency_file_path["NLP"], "rb") as openfile:
        nlp = pickle.load(openfile)

    all_token_without_stop_words = process_to_vectorize_documents(doc_link['Document'], nlp)
    
    vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1,3))
    normalizer = StandardScaler(with_mean=False)
    vectors = vectorize_all_docs(all_token_without_stop_words, vectorizer)
    links = get_links(doc_link['Link'])

    dump_file(dependency_file_path["VECTORIZER"], vectorizer)
    dump_file(dependency_file_path["NORMALIZER"], normalizer)
    dump_file(dependency_file_path["VECTORS"], vectors)
    dump_file(dependency_file_path["LINKS"], links)

def web_scrapper(root):
    pass