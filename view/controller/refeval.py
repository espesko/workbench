from model import Details, DetailView
from __init__ import controller


#----------------------------------------------------------------------
def convert_details_results(results):
    """
    Convert query results to a list of DetailView objects
    This is where the control logic should be placed when things become more complex
    """
    details = []
    for r in results:
        detail = DetailView(r.id, r.gene, r.hgvs_cdna, r.observed_genotype,
                            r.reason_for_vardb_class, r.effect, r.bic,
                            r.hgmd_pro, r.sift, r.mutation_taster)
        details.append(detail)
    return details
    
#----------------------------------------------------------------------
def add_details_record(data, export=False):
    """
    Data should be an object of class DetailView
    """
    detail = Details()
    detail.gene = data["gene"]
    detail.hgvs_cdna = data["hgvs_cdna"]
    detail.observed_genotype = data["observed_genotype"]
    detail.reason_for_vardb_class = data["reason_for_vardb_class"]
    detail.effect = data["effect"]
    detail.bic = data["bic"]
    detail.hgmd_pro = data["hgmd_pro"]
    detail.sift = data["sift"]
    detail.mutation_taster = data["mutation_taster"]
    
    if export:
        session = controller.connect_to_export_file()
    else:
        session = controller.connect_to_database()
    session.add(detail)
    session.commit()
    session.close()

#----------------------------------------------------------------------
def update_details_record(id, data):
    """
    Update a prediction record
    Data should be an object of class DetailView
    """
    session = controller.connect_to_database()
    record = session.query(Details).filter_by(id=id).one()

    record.gene = data["gene"]
    record.hgvs_cdna = data["hgvs_cdna"]
    record.observed_genotype = data["observed_genotype"]
    record.reason_for_vardb_class = data["reason_for_vardb_class"]
    record.effect = data["effect"]
    record.bic = data["bic"]
    record.hgmd_pro = data["hgmd_pro"]
    record.sift = data["sift"]
    record.mutation_taster = data["mutation_taster"]
  
    session.commit()
    session.close()

#----------------------------------------------------------------------
def get_details_record(gene, hgvs_cdna):
    """
    Get all details records and return them
    """
    session = controller.connect_to_database()
    result = session.query(Details).filter_by(gene=gene, hgvs_cdna=hgvs_cdna).all()
    details = convert_details_results(result)
    session.close()
    return details

#----------------------------------------------------------------------
def get_all_details_records():
    """
    Get all details records and return them
    """
    session = controller.connect_to_database()
    result = session.query(Details).all()
    details = convert_details_results(result)
    session.close()
    return details

if __name__ == "__main__":
    #print get_details_record("BRCA1", "c.1067A>G")
    print get_all_details_records()
