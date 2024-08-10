from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import get_db
from models import Project
from utils import populate_database, get_faiss_index, query_faiss_index
import numpy as np
app = FastAPI()

@app.get('/')
def welcome():
    return {'message': 'Welcome to backend similarity checker. 👋' }

@app.on_event("startup")
def startup_event():
    # used with iterators that  use yield keyword
    db = next(get_db())
    print('Buiding index ....')
    get_faiss_index(db)
    print('Built the index')

@app.get("/projects/")
def read_projects(skip = 0, limit = 10, db = Depends(get_db)):
    projects = db.query(Project).offset(skip).limit(limit).all()
    return projects  

@app.get('/project/similar')
def get_similar_projects(title:str = '', abstract: str = '', category:str = '', k:int = 5, db:Session = Depends(get_db)):
    query = np.array([f"{title} {abstract} {category}"])

    similar_project_ids, distances, similarity_scores = query_faiss_index(query, k)

    print(similar_project_ids, similarity_scores)
    
    projects = db.query(Project).filter(Project.project_id.in_(similar_project_ids)).all()
    return list(zip(projects, similarity_scores))

@app.get("/build-db/")
def build_db(db = Depends(get_db)):
    msg = populate_database(db, 1, 2000)
    return msg