from fastapi import FastAPI, HTTPException
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import pickle
import pathlib
import platform

DEFAULT_PICKLE_FILEPATH_TYPE = pathlib.PosixPath

dependency_file_path = {
    "VECTORIZER" : "./vectorizer.pk",
    "VECTORS" : "./vectors.pk",
    "LINKS" : "./links.pk",
    "NORMALIZER" : "./normalizer.pk",
    # "NLP" : "./nlp.pk"
}

dependencies = {}

def dependency_loader():
    if platform.system()=="Windows":
        pathlib.PosixPath = pathlib.WindowsPath
    for filename,filepath in dependency_file_path.items():
        try:
            with open(filepath, "rb") as file:
                print(f"Pickling {filename}")
                dependencies[filename] = pickle.load(file)
                print(f"{filename} unpicked!")
        except Exception as E:
            raise RuntimeError(f"Exception:{E}")
    print("Changing PosixPath back")
    pathlib.PosixPath = DEFAULT_PICKLE_FILEPATH_TYPE
    print("PosixPath changed back")

# Load Dependencies
dependency_loader()
print("loaded dependencies:")
print(dependencies)
# server = FastAPI()