import pandas as pd
import re

def preprocess_document(url):
    data = pd.read_excel(url)

    rows = []
    for i in range(len(data[0])):
        rows.append([data[0][i], data[1][i]])

    data_act = pd.DataFrame(rows, columns=['Link', 'Document'])

    link_to_document_dict = {}
    for i in range(len(data_act['Document'])):
        processed_doc = re.sub(r'\s{2,}', ' ', data_act['Document'][i])
        link_to_document_dict[data_act['Link'][i]] = processed_doc

    required_rows = []
    for i in link_to_document_dict.keys():
        required_rows.append([i, link_to_document_dict[i]])

    Link_to_Doc = pd.DataFrame(rows, columns=['Link', 'Document'])

    for i in range(len(Link_to_Doc['Document'])):
        lower_than_upper_split = re.sub(r"([a-z\.!?])([A-Z])", r"\1 \2", Link_to_Doc['Document'][i])
        upper_than_lower_split = re.sub(r"([A-Z\.!?]{2,})([A-Z]{1}[a-z]{2,})", r"\1 \2", lower_than_upper_split)
        bracket_before = re.sub(r"([)])([A-Z])", r"\1 \2", upper_than_lower_split)
        bracket_after = re.sub(r"([a-z])([(])", r"\1 \2", bracket_before)
        rmv_smbl = re.sub(r'[^A-Za-z\n@]', ' ', bracket_after)
        rmv_spcs = re.sub(r'\s{2,}', ' ', rmv_smbl)
        Link_to_Doc['Document'][i] = rmv_spcs
    
    filename = url.split("/")[-1]

    Link_to_Doc.to_excel(filename, index=False)

    return f'./{filename}'