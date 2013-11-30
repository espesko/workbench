from model import VarDB, VarDBView
from __init__ import controller

#----------------------------------------------------------------------
def convert_vardb_results(results):
    """
    Convert query results to a list of VarDBView objects
    This is where the control logic should be placed when things become more complex
    """
    vdbs = []
    for r in results:
        vdb = VarDBView(r.id, r.gene, r.variant, r.var_db, r.summary, r.last_check)
        vdbs.append(vdb)
    return vdbs
    
#----------------------------------------------------------------------
def add_vardb_record(data, export=False):
    """
    Data should be an object of class VarDBView
    """
    vdb = VarDB()
    vdb.gene = data["gene"]
    vdb.variant = data["variant"]
    vdb.var_db = data["var_db"]
    vdb.summary = data["summary"]
    vdb.last_check = data["last_check"]
    
    if export:
        session = controller.connect_to_export_file()
    else:
        session = controller.connect_to_database()
    session.add(vdb)
    session.commit()
    session.close()

#----------------------------------------------------------------------
def update_vardb_record(data):
    """
    Update a vardb record
    Data should be an object of class VarDBView
    """
    session = controller.connect_to_database()
    record = session.query(VarDB).filter_by(id=data["id"]).one()

    record.gene = data["gene"]
    record.variant = data["variant"]
    record.var_db = data["var_db"]
    record.summary = data["summary"]
    record.last_check = data["last_check"]

    session.commit()
    session.close()

#----------------------------------------------------------------------
def get_all_vardb_records():
    """
    Get all vardb records and return them
    """
    session = controller.connect_to_database()
    result = session.query(VarDB).all()
    vdbs = convert_vardb_results(result)
    session.close()
    return vdbs


#print get_all_vardb_records()
