from model import ExternalDB, ExtDBView
from __init__ import controller

#----------------------------------------------------------------------
def convert_extdb_results(results):
    """
    Convert query results to a list of ExtDBView objects
    This is where the control logic should be placed when things become more complex
    """
    extdbs = []
    for r in results:
        extdb = ExtDBView(r.id, r.gene, r.variant, r.bic, r.hgmd_pro,
                        r.lovd, r.clin_var, r.omim, r.db_snp)
        extdbs.append(extdb)
    return extdbs
    
#----------------------------------------------------------------------
def add_extdb_record(data, export=False):
    """
    Data should be an object of class ExtDBView
    """
    extdb = ExternalDB()
    extdb.gene = data["gene"]
    extdb.variant = data["variant"]
    extdb.bic = data["bic"]
    extdb.hgmd_pro = data["hgmd_pro"]
    extdb.lovd = data["lovd"]
    extdb.clin_var = data["clin_var"]
    extdb.omim = data["omim"]
    extdb.db_snp = data["db_snp"]
    
    if export:
        session = controller.connect_to_export_file()
    else:
        session = controller.connect_to_database()
    session.add(extdb)
    session.commit()
    session.close()

#----------------------------------------------------------------------
def update_extdb_record(data):
    """
    Update a ExternalDB record
    Data should be an object of class FreqView
    """
    session = controller.connect_to_database()
    record = session.query(ExternalDB).filter_by(id=data["id"]).one()

    record.gene = data["gene"]
    record.variant = data["variant"]
    record.bic = data["bic"]
    record.hgmd_pro = data["hgmd_pro"]
    record.lovd = data["lovd"]
    record.clin_var = data["clin_var"]
    record.omim = data["omim"]
    record.db_snp = data["db_snp"]

    session.commit()
    session.close()

#----------------------------------------------------------------------
def get_all_extdb_records():
    """
    Get all ExternalDB records and return them
    """
    session = controller.connect_to_database()
    result = session.query(ExternalDB).all()
    extdbs = convert_extdb_results(result)
    session.close()
    return extdbs

#print get_all_extdb_records()
