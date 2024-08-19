import platform
import pathlib
import pickle
import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler

model_binaries_file_path = {
    "VECTORIZER" : "./vectorizer.pk",
    "VECTORS" : "./vectors.pk",
    "LINKS" : "./links.pk",
    "NORMALIZER" : "./normalizer.pk",
    "NLP" : "./nlp_win.pk" if platform.system()=="Windows" else "./nlp.pk"
}

def model_binaries_loader():
    dependencies = {}

    DEFAULT_PICKLE_FILEPATH_TYPE = pathlib.PosixPath
    if platform.system()=="Windows":
        pathlib.PosixPath = pathlib.WindowsPath

    for filename,filepath in model_binaries_file_path.items():
        try:
            with open(filepath, "rb") as file:
                dependencies[filename] = pickle.load(file)
                print(f"{filename} loaded!")
        except Exception as E:
            raise RuntimeError(f"Exception:{E}")
        
    pathlib.PosixPath = DEFAULT_PICKLE_FILEPATH_TYPE

    return dependencies

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

def dump_file(filename, mode):
    with open(filename, mode) as fin:
        pickle.dump(filename, fin)

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

def update_model_binaries_from_document(doc_file: str):
    doc_link = pd.read_excel(doc_file)

    with open(model_binaries_file_path["NLP"], "rb") as openfile:
        nlp = pickle.load(openfile)

    all_token_without_stop_words = process_to_vectorize_documents(doc_link['Document'], nlp)
    
    vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1,1))
    normalizer = StandardScaler(with_mean=False)
    vectors = vectorize_all_docs(all_token_without_stop_words, vectorizer)
    links = get_links(doc_link['Link'])

    dump_file(model_binaries_file_path["VECTORIZER"], vectorizer)
    dump_file(model_binaries_file_path["NORMALIZER"], normalizer)
    dump_file(model_binaries_file_path["VECTORS"], vectors)
    dump_file(model_binaries_file_path["LINKS"], links)

__all__ = ["model_binaries_loader"]