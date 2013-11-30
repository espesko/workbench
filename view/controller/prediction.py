from model import Prediction, PredView
from __init__ import controller

#----------------------------------------------------------------------
def convert_pred_results(results):
    """
    Convert query results to a list of PredView objects
    This is where the control logic should be placed when things become more complex
    """
    preds = []
    for r in results:
        pred = PredView(r.id, r.gene, r.variant, r.type_of_mutation, r.comment)
        preds.append(pred)
    return preds
    
#----------------------------------------------------------------------
def add_pred_record(data, export=False):
    """
    Data should be an object of class PredView
    """
    pred = Prediction()
    pred.gene = data["gene"]
    pred.variant = data["variant"]
    pred.type_of_mutation = data["type_of_mutation"]
    pred.comment = data["comment"]
    
    if export:
        session = controller.connect_to_export_file()
    else:
        session = controller.connect_to_database()
    session.add(pred)
    session.commit()
    session.close()

#----------------------------------------------------------------------
def update_pred_record(data):
    """
    Update a prediction record
    Data should be an object of class PredView
    """
    session = controller.connect_to_database()
    record = session.query(Prediction).filter_by(id=data["id"]).one()

    record.gene = data["gene"]
    record.variant = data["variant"]
    record.type_of_mutation = data["type_of_mutation"]
    record.comment = data["comment"]
  
    session.commit()
    session.close()

#----------------------------------------------------------------------
def get_all_pred_records():
    """
    Get all prediction records and return them
    """
    session = controller.connect_to_database()
    result = session.query(Prediction).all()
    preds = convert_pred_results(result)
    session.close()
    return preds

   
#print get_all_pred_records()
