from model import References, RefView
from __init__ import controller

#----------------------------------------------------------------------
def convert_ref_results(results):
    """
    Convert query results to a list of RefView objects
    This is where the control logic should be placed when things become more complex
    """
    refs = []
    for r in results:
        ref = RefView(r.id, r.gene, r.variant, r.source, r.references,
                        r.previous_evaluations, r.high_quality_evidence)
        refs.append(ref)
    return refs
    
#----------------------------------------------------------------------
def add_ref_record(data, export=False):
    """
    Data should be an object of class RefView
    """
    ref = References()
    ref.gene = data["gene"]
    ref.variant = data["variant"]
    ref.source = data["source"]
    ref.references = data["references"]
    ref.previous_evaluations = data["previous_evaluations"]
    ref.high_quality_evidence = data["high_quality_evidence"]
    
    if export:
        session = controller.connect_to_export_file()
    else:
        session = controller.connect_to_database()
    session.add(ref)
    session.commit()
    session.close()

#----------------------------------------------------------------------
def update_ref_record(data):
    """
    Update a references record
    Data should be an object of class RefView
    """
    session = controller.connect_to_database()
    record = session.query(References).filter_by(id=data["id"]).one()

    record.gene = data["gene"]
    record.variant = data["variant"]
    record.source = data["source"]
    record.references = data["references"]
    record.previous_evaluations = data["previous_evaluations"]
    record.high_quality_evidence = data["high_quality_evidence"]

    session.commit()
    session.close()

#----------------------------------------------------------------------
def get_all_ref_records():
    """
    Get all References records and return them
    """
    session = controller.connect_to_database()
    result = session.query(References).all()
    refs = convert_ref_results(result)
    session.close()
    return refs


#print get_all_ref_records()
