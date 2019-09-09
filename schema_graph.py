from sqlalchemy import MetaData
from sqlalchemy_schemadisplay import create_schema_graph
from app import app
from app import db
from sqlalchemy_schemadisplay import create_uml_graph
from sqlalchemy.orm import class_mapper

def GenerateSchema():
    # create the pydot graph object by autoloading all tables via a bound metadata object
    graph = create_schema_graph(metadata=MetaData(app.config['SQLALCHEMY_DATABASE_URI']),
    show_datatypes=False, # The image would get nasty big if we'd show the datatypes
    show_indexes=False, # ditto for indexes
    rankdir='LR', # From left to right (instead of top to bottom)
    concentrate=False # Don't try to join the relation lines together
    )
    graph.write_png('dbschema.png') # write out the file



    if __name__ == '__main__':   
        GenerateSchema()