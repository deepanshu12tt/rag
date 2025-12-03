import faiss
import numpy as np
import os
import pickle

INDEX_PATH = "faiss_index.bin"
IDMAP_PATH = "faiss_idmap.pkl"


class VectorIndex:
    def __init__(self, dim):
        self.dim = dim 
        self.index = faiss.IndexFlatL2(dim)

        if os.path.exists(INDEX_PATH):
            faiss.read_index_into(self.index, INDEX_PATH)

        if os.path.exists(IDMAP_PATH):
            with open(IDMAP_PATH, "rb") as f:
                self.id_map = pickle.load(f)
        else:
            self.id_map = []  

    def save(self):
        faiss.write_index(self.index, INDEX_PATH)
        with open(IDMAP_PATH, "wb") as f:
            pickle.dump(self.id_map, f)

    def add(self, vector, int_id):
        self.index.add(np.array([vector]).astype("float32"))
        self.id_map.append(int_id)
        self.save()

    def search(self, vector, k=5):
        vector = np.array([vector]).astype("float32")
        D, I = self.index.search(vector, k)
        result = []
        for row in I[0]:
            if row < len(self.id_map):
                result.append(self.id_map[row])
        return result
