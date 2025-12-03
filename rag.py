import uuid
import numpy as np
from db import init_db, next_int_id, insert_chunk, fetch_chunks_by_ids
from embedder import Embedder
from indexer import VectorIndex


class SimpleRAG:
    def __init__(self):
        self.conn = init_db()
        self.embedder = Embedder()
        self.index = VectorIndex(self.embedder.dim)

    def chunk(self, text, max_chars=500):
        if len(text) <= max_chars:
            return [text]
        return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

    def ingest(self, text):
        chunks = self.chunk(text)
        vectors = self.embedder.embed(chunks)

        for i, ch in enumerate(chunks):
            msg_id = str(uuid.uuid4())
            int_id = next_int_id(self.conn)

            insert_chunk(self.conn, msg_id, int_id, ch)
            self.index.add(vectors[i], int_id)

        print(f"Ingested {len(chunks)} chunks.")

    def query(self, question, top_k=5):
        q_vec = self.embedder.embed([question])[0]
        ids = self.index.search(q_vec, k=top_k)

        chunks = fetch_chunks_by_ids(self.conn, ids)
        return "\n---\n".join(chunks)
