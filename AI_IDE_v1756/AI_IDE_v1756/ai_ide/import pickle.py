from importlib import metadata
from vector_smanager import VectorStoreManager
import pickle

vsm = VectorStoreManager()

store = vsm._load_faiss_store()
#with open("AppData/VSM_1_Data/index.pkl", "rb") as f:
#    data = pickle.load(f)

