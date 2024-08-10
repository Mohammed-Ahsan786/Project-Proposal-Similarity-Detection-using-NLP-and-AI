from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-mpnet-base-v2')

def get_embedding(text:list):
    embedding = model.encode(text, convert_to_tensor = False)
    return embedding

def get_similarity(embedding1, embedding2):
    return util.cos_sim(embedding1, embedding2).item()


