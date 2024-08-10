import faiss
import os
from .language_model import get_embedding, get_similarity
from models import Project
import pickle
import numpy as np
# file to store the vector indexes
INDEX_FILE = 'index/projects_index.bin'
# this file stores ids of mapped project in binary file
MAPPING_FILE = 'index/project_id_mappings.pkl'

# This file will store the embeddings
EMBEDDINGS_FILE = 'index/embeddings.npy'

index = None
project_id_to_faiss_idx = {}
faiss_idx_to_project_id = {}

def get_faiss_index(db):
    global index, project_id_to_faiss_idx, faiss_idx_to_project_id
    # if index is already built then return it
    if index is not None:
        return index
    
    # check if index file exists 
    if os.path.exists(INDEX_FILE) and os.path.exists(MAPPING_FILE):
        index = faiss.read_index(INDEX_FILE)
        # read the pickle file and build the dictionary
        with open(MAPPING_FILE, 'rb') as f:
            project_id_to_faiss_idx = pickle.load(f)
            faiss_idx_to_project_id = {val:key for key,val in project_id_to_faiss_idx.items()}
        return index

    else:
        index = build_faiss_index(db)
        return index

def build_faiss_index(db):
    global index, project_id_to_faiss_idx, faiss_idx_to_project_id
    if os.path.exists(EMBEDDINGS_FILE):
        embeddings = np.load(EMBEDDINGS_FILE)
    else:
        # get all the projects
        projects = db.query(Project).all()
        # combine the texts
        texts = [f'{project.title} {project.abstract} {project.category}' for project in projects]
        embeddings = get_embedding(texts)
        # Save embeddings
        np.save(EMBEDDINGS_FILE, embeddings)

    # get dimensions or vector size 784 for our project [depends on model]
    dimension = embeddings.shape[1]
    # build the index
    index = faiss.IndexFlatL2(dimension)
    # Add embeddings to the index
    index.add(embeddings)

    # Map the project_ids to indices in faiss index
    project_id_to_faiss_idx = {project.project_id : idx for idx, project in enumerate(projects)}
    faiss_idx_to_project_id = {idx: project_id for project_id, idx   in project_id_to_faiss_idx.items()}

    # save index and mappings
    faiss.write_index(index, INDEX_FILE)
    with open(MAPPING_FILE, 'wb') as f:
        pickle.dump(project_id_to_faiss_idx, f)

    return index
def load_embeddings():
    # Load embeddings
    embeddings = np.load(EMBEDDINGS_FILE)
    return embeddings

def query_faiss_index(query, k = 5):
    query_embedding = get_embedding(query)
    distances, indices = index.search(query_embedding, k)
    # map FAISS index to project_ids
    result_ids = [faiss_idx_to_project_id[idx] for idx in indices[0] if idx in faiss_idx_to_project_id]

    # get the saved embeddings 
    embeddings = np.load(EMBEDDINGS_FILE)
    # calculate simialrity scores
    similarity_scores = [get_similarity(embeddings[idx], query_embedding) for idx in indices[0] if idx in faiss_idx_to_project_id]

    return result_ids, distances, similarity_scores
