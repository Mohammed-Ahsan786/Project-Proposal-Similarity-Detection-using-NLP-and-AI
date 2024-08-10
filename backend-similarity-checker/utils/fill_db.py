import requests
from models import Project
# Base URL for fetching data
base_url = "https://datasets-server.huggingface.co/rows?dataset=universeTBD%2Farxiv-abstracts-large&config=default&split=train&offset={offset}&length={length}"

# Function to fetch records from the API
def get_records_from_api(length, offset):
    response = requests.get(base_url.format(length = length, offset = offset))
    if response.status_code == 200:
        return response.json()['rows']
    else:
        raise HTTPException(status_code = 500, detail = "Failed to fetch from API.")

# function to populate the DB table

def populate_database(db, group_id, records_to_fetch):
    # checking the existing no. of projects
    projects_count = db.query(Project).count()
    if projects_count >= 100:
        return "Database already has sufficent projects"
    
    offset = 0
    length = 100
    all_records = []
    while len(all_records) < records_to_fetch:
        records = get_records_from_api(length, offset)
        all_records.extend(records)
        offset += length

    for record in all_records:
        new_project = Project(
            title=record['row']['title'],
            abstract=record['row']['abstract'],
            category=record['row']['categories'],
            group_id=group_id
        )
        db.add(new_project)
        db.commit()

        # refresh the new_project to get updated data
        db.refresh(new_project)
        
    return {"message": "Projects add succesfully"}



