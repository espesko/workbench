from model import Sample, SamplView, VarDB, VarDBView, Frequency, FreqView
from model import ExternalDB, ExtDBView, Prediction, PredView, Details, DetailView
from model import References, RefView
import sample
import vardb
import frequency
import external_db
import prediction
import details
import references

def export_samples():
    records = sample.get_all_sample_records()
    for record in records:
        sample.add_sample_record(record, export=True)

def export_vardbs():
    records = vardb.get_all_vardb_records()
    for record in records:
        vardb.add_vardb_record(record, export=True)

def export_frequencies():
    records = frequency.get_all_freq_records()
    for record in records:
        frequency.add_freq_record(record, export=True)

def export_external_dbs():
    records = external_db.get_all_extdb_records()
    for record in records:
        external_db.add_extdb_record(record, export=True)

def export_predictions():
    records = prediction.get_all_pred_records()
    for record in records:
        prediction.add_pred_record(record, export=True)

def export_details():
    records = details.get_all_details_records()
    for record in records:
        details.add_details_record(record, export=True)

def export_references():
    records = references.get_all_ref_records()
    for record in records:
        references.add_ref_record(record, export=True)

def export_all():
    export_samples()
    export_vardbs()
    export_frequencies()
    export_external_dbs()
    export_predictions()
    export_details()
    export_references()
    from model.export import filename
    return filename

if __name__ == "__main__":
    print export_all()
