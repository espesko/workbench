from model import Frequency, FreqView
from __init__ import controller

#----------------------------------------------------------------------
def convert_freq_results(results):
    """
    Convert query results to a list of FreqView objects
    This is where the control logic should be placed when things become more complex
    """
    freqs = []
    for r in results:
        freq = FreqView(r.id, r.gene, r.variant, r.norvariome, r.esp65000,
                        r.thousand_g, r.contradictory)
        freqs.append(freq)
    return freqs
    
#----------------------------------------------------------------------
def add_freq_record(data, export=False):
    """
    Data should be an object of class FreqView
    """
    freq = Frequency()
    freq.gene = data["gene"]
    freq.variant = data["variant"]
    if str(data["norvariome"]).isdigit():
        freq.norvariome = data["norvariome"]
    if str(data["esp65000"]).isdigit():
        freq.esp65000 = data["esp65000"]
    if str(data["thousand_g"]).isdigit():
        freq.thousand_g = data["thousand_g"]
    freq.contradictory = data["contradictory"]
    
    if export:
        session = controller.connect_to_export_file()
    else:
        session = controller.connect_to_database()
    session.add(freq)
    session.commit()
    session.close()

#----------------------------------------------------------------------
def update_freq_record(data):
    """
    Update a frequency record
    Data should be an object of class FreqView
    """
    session = controller.connect_to_database()
    record = session.query(Frequency).filter_by(id=data["id"]).one()

    record.gene = data["gene"]
    record.variant = data["variant"]
    if str(data["norvariome"]).isdigit():
        record.norvariome = data["norvariome"]
    if str(data["esp65000"]).isdigit():
        record.esp65000 = data["esp65000"]
    if str(data["thousand_g"]).isdigit():
        record.thousand_g = data["thousand_g"]
    record.contradictory = data["contradictory"]

    session.commit()
    session.close()

#----------------------------------------------------------------------
def get_all_freq_records():
    """
    Get all frequency records and return them
    """
    session = controller.connect_to_database()
    result = session.query(Frequency).all()
    freqs = convert_freq_results(result)
    session.close()
    return freqs

#print get_all_freq_records()
