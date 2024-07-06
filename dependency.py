import platform
import pathlib
import pickle
import spacy

_dependency_file_path = {
    "VECTORIZER" : "./vectorizer.pk",
    "VECTORS" : "./vectors.pk",
    "LINKS" : "./links.pk",
    "NORMALIZER" : "./normalizer.pk",
    # "NLP" : "./nlp.pk"
}

def dependency_loader():
    dependencies = {}

    DEFAULT_PICKLE_FILEPATH_TYPE = pathlib.PosixPath
    if platform.system()=="Windows":
        pathlib.PosixPath = pathlib.WindowsPath

    for filename,filepath in _dependency_file_path.items():
        try:
            with open(filepath, "rb") as file:
                dependencies[filename] = pickle.load(file)
                print(f"{filename} loaded!")
        except Exception as E:
            raise RuntimeError(f"Exception:{E}")
        
    pathlib.PosixPath = DEFAULT_PICKLE_FILEPATH_TYPE

    return dependencies

__all__ = ["dependency_loader"]