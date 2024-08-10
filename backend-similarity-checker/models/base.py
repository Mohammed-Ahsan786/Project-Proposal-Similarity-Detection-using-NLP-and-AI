from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

class CustomMetaData(MetaData):
    def __init__(self, *args, **kwargs):
        if 'schema' not in kwargs:
            kwargs['schema'] = 'project_db'
        super().__init__(*args, **kwargs)

metadata = CustomMetaData()
Base = declarative_base(metadata=metadata)