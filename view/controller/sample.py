from model import Sample, SamplView
from __init__ import controller

#----------------------------------------------------------------------
def convert_sample_results(results):
    """
    Convert query results to a list of SamplView objects
    This is where the control logic should be placed when things become more complex
    """
    if not results:
        return [None]
    samples = []
    for r in results:
        sample = SamplView(id, r.sample, r.panel, r.sample_taken, r.genotyping,
                 r.variant_calling, r.qc_status, r.qc_report, r.coverage)
        samples.append(sample)
    return samples
    
#----------------------------------------------------------------------
def add_sample_record(data, export=False):
    """
    Data should be an object of class SamplView
    """
    sample = Sample()
    sample.sample = data["sample"]
    sample.panel = data["panel"]
    sample.sample_taken = data["sample_taken"]
    sample.genotyping = data["genotyping"]
    sample.variant_calling = data["variant_calling"]
    sample.qc_status = data["qc_status"]
    sample.qc_report = data["qc_report"]
    sample.coverage = data["coverage"]

    if export:
        session = controller.connect_to_export_file()
    else:
        session = controller.connect_to_database()
    session.add(sample)
    session.commit()
    session.close()

#----------------------------------------------------------------------
def update_sample_record(data):
    """
    Update a vardb record
    Data should be an object of class SampleView
    """
    session = controller.connect_to_database()
    record = session.query(Sample).filter_by(id=data["id"]).one()

    record = Sample()
    record.sample = data["sample"]
    record.panel = data["panel"]
    record.sample_taken = data["sample_taken"]
    record.genotyping = data["genotyping"]
    record.variant_calling = data["variant_calling"]
    record.qc_status = data["qc_status"]
    record.qc_report = data["qc_report"]
    record.coverage = data["coverage"]

    session.commit()
    session.close()

#----------------------------------------------------------------------
def get_sample_record(sample):
    """
    Get all sample records and return them
    """
    session = controller.connect_to_database()
    result = session.query(Sample).filter_by(sample=sample).all()
    sample = convert_sample_results(result)
    session.close()
    return sample[0]

#----------------------------------------------------------------------
def get_all_sample_records():
    """
    Get all sample records and return them
    """
    session = controller.connect_to_database()
    result = session.query(Sample).all()
    samples = convert_sample_results(result)
    session.close()
    return samples


#print get_sample_record("000001A")
#print get_all_sample_records()
