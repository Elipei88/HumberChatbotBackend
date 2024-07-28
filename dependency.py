import platform
import pathlib
import pickle
import spacy

dependency_file_path = {
    "VECTORIZER" : "./vectorizer.pk",
    "VECTORS" : "./vectors.pk",
    "LINKS" : "./links.pk",
    "NORMALIZER" : "./normalizer.pk",
    "NLP" : "./nlp_win.pk" if platform.system()=="Windows" else "./nlp.pk"
}

def dependency_loader():
    dependencies = {}

    DEFAULT_PICKLE_FILEPATH_TYPE = pathlib.PosixPath
    if platform.system()=="Windows":
        pathlib.PosixPath = pathlib.WindowsPath

    for filename,filepath in dependency_file_path.items():
        try:
            with open(filepath, "rb") as file:
                dependencies[filename] = pickle.load(file)
                print(f"{filename} loaded!")
        except Exception as E:
            raise RuntimeError(f"Exception:{E}")
        
    pathlib.PosixPath = DEFAULT_PICKLE_FILEPATH_TYPE

    return dependencies

__all__ = ["dependency_loader"]