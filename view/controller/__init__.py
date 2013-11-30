from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#from model import VarDB, Frequency, ExternalDB, Prediction, Details
from model import db_name

class Controller(object):

    def connect_to_database(self):
        """
        Connect to database and return a Session object
        """
        engine = create_engine(db_name)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session
    
    def delete_record(self, table, id):
        """
        Delete a record from table <table>
        """
        session = connectToDatabase()
        record = session.query(table).filter_by(id=id).one()
        session.delete(record)
        session.commit()
        session.close()
    
    def connect_to_export_file(self):
        """
        Create an export file and return a Session object
        """
        from model.export import export_db

        engine = create_engine(export_db)
        Session = sessionmaker(bind=engine)
        session = Session()
        session.export_db = export_db
        return session
    
controller = Controller()
#print "Controller created:", controller
    
