import datetime
from sqlalchemy import Table, Column, create_engine
from sqlalchemy import Integer, ForeignKey, String, Unicode, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relation

now = datetime.datetime.today()
filename = "export%.4d%.2d%.2d%.2d%.2d.db" % (now.year, now.month,
                                              now.day, now.hour, now.minute)
export_db = "sqlite:///" + filename

engine = create_engine(export_db)
DeclarativeBase = declarative_base(engine)
metadata = DeclarativeBase.metadata


class RefView(dict):
     def __init__(self, id, gene, variant, source, references,
                  previous_evaluations, high_quality_evidence):
        dict.__init__(self)
        self["id"] = id  # unique row id from database
        self["gene"] = gene
        self["variant"] = variant
        self["source"] = source
        self["references"] = references
        self["previous_evaluations"] = previous_evaluations
        self["high_quality_evidence"] = high_quality_evidence
        self.is_changed = False
     def __del__(self):
        if self.is_changed:
            print "%s %d is changed" % (type(self), self["id"])

class References(DeclarativeBase):
    __tablename__ = "references"
    
    id = Column(Integer, primary_key=True)
    gene = Column("gene", String(20))
    variant = Column("variant", String(20))
    source = Column("source", String(50))
    references = Column("references", String(200))
    previous_evaluations = Column("previous_evaluations", String(200))
    high_quality_evidence = Column("high_quality_evidence", String(50))
        
       
class SamplView(dict):
    def __init__(self, id, sample, panel, sample_taken, genotyping,
                 variant_calling, qc_status, qc_report, coverage):
        dict.__init__(self)
        self["id"] = id  # unique row id from database
        self["sample"] = sample
        self["panel"] = panel
        self["sample_taken"] = sample_taken
        self["genotyping"] = genotyping
        self["variant_calling"] = variant_calling
        self["qc_status"] = qc_status
        self["qc_report"] = qc_report
        self["coverage"] = coverage
        self.is_changed = False
    def __del__(self):
        if self.is_changed:
            print "%s %d is changed" % (type(self), self["id"])
 
class Sample(DeclarativeBase):
    __tablename__ = "sample"
    
    id = Column(Integer, primary_key=True)
    sample = Column("sample", String(20))
    panel = Column("panel", String(30))
    sample_taken = Column("sample_taken", Date)
    genotyping = Column("genotyping", String(50))
    variant_calling = Column("variant_calling", String(50))
    qc_status = Column("qc_status", String(20))
    qc_report = Column("qc_report", String(50))
    coverage = Column("coverage", String(50))
    
       
class VarDBView(dict):
    VALIDITY_THRESHOLD = datetime.timedelta(180)
    def __init__(self, id, gene, variant, var_db, summary, last_check):
        dict.__init__(self)
        self["id"] = id  # unique row id from database
        self["gene"] = gene
        self["variant"] = variant
        self["var_db"] = var_db
        self["summary"] = summary
        self["last_check"] = last_check
        self["valid"] = self.set_validity()
        self.is_changed = False
    def __del__(self):
        if self.is_changed:
            print "%s %d is changed" % (type(self), self["id"])
    def set_validity(self):
        age = datetime.date.today() - self["last_check"]
        return (age < self.VALIDITY_THRESHOLD)
 
class VarDB(DeclarativeBase):
    __tablename__ = "var_db"
    
    id = Column(Integer, primary_key=True)
    gene = Column("gene", String(20))
    variant = Column("variant", String(20))
    var_db = Column("var_db", String(20))
    summary = Column("summary", String(500))
    last_check = Column("last_check", Date)
    
       
class FreqView(dict):
    NEUTRALITY_THRESHOLD = 0.01
    def __init__(self, id, gene, variant, norvariome, esp65000,
                 thousand_g, contradictory):
        dict.__init__(self)
        self["id"] = id  # unique row id from database
        self["gene"] = gene
        self["variant"] = variant
        self["norvariome"] = norvariome
        self["esp65000"] = esp65000
        self["thousand_g"] = thousand_g
        self["contradictory"] = contradictory
        self["neutral"] = self.set_neutrality()
        self.is_changed = False
    def __del__(self):
        if self.is_changed:
            print "%s %d is changed" % (type(self), self["id"])
    def set_neutrality(self):
        max_val = max(self["norvariome"], self["esp65000"],
                      self["thousand_g"])
        return (max_val > self.NEUTRALITY_THRESHOLD)
 
class Frequency(DeclarativeBase):
    __tablename__ = "frequency"
    
    id = Column(Integer, primary_key=True)
    gene = Column("gene", String(20))
    variant = Column("variant", String(20))
    norvariome = Column("norvariome", Numeric)
    esp65000 = Column("esp65000", Numeric)
    thousand_g = Column("1000g", Numeric)
    contradictory = Column("contradictory", String(500))
    
          
class ExtDBView(dict):
    def __init__(self, id, gene, variant, bic, hgmd_pro, lovd,
                 clin_var, omim, db_snp):
        dict.__init__(self)
        self["id"] = id  # unique row id from database
        self["gene"] = gene
        self["variant"] = variant
        self["bic"] = bic
        self["hgmd_pro"] = hgmd_pro
        self["lovd"] = lovd
        self["clin_var"] = clin_var
        self["omim"] = omim
        self["db_snp"] = db_snp
        self.is_changed = False
    def __del__(self):
        if self.is_changed:
            print "%s %d is changed" % (type(self), self["id"])
        
        
class ExternalDB(DeclarativeBase):
    __tablename__ = "external_db"
    
    id = Column(Integer, primary_key=True)
    gene = Column("gene", String(20))
    variant = Column("variant", String(20))
    bic = Column("bic", String(100))
    hgmd_pro = Column("hgmd_pro", String(100))
    lovd = Column("lovd", String(100))
    clin_var = Column("clin_var", String(100))
    omim = Column("omim", String(100))
    db_snp = Column("db_snp", String(100))

    
class PredView(dict):
    def __init__(self, id, gene, variant, type_of_mutation, comment):
        dict.__init__(self)
        self["id"] = id  # unique row id from database
        self["gene"] = gene
        self["variant"] = variant
        self["type_of_mutation"] = type_of_mutation
        self["comment"] = comment
        self.is_changed = False
    def __del__(self):
        if self.is_changed:
            print "%s %d is changed" % (type(self), self["id"])

#pv = PredView(1, 2, 3, 4, 5)
#print pv["comment"]
        
class Prediction(DeclarativeBase):
    __tablename__ = "prediction"
    
    id = Column(Integer, primary_key=True)
    gene = Column("gene", String(20))
    variant = Column("variant", String(20))
    type_of_mutation = Column("type_of_mutation", String(100))
    comment = Column("comment", String(100))
    
          
class DetailView(dict):
    def __init__(self, id, gene, hgvs_cdna, observed_genotype,
                 reason_for_vardb_class, effect, bic,
                 hgmd_pro, sift, mutation_taster):
        dict.__init__(self)
        self["id"] = id  # unique row id from database
        self["gene"] = gene
        self["hgvs_cdna"] = hgvs_cdna
        self["observed_genotype"] = observed_genotype
        self["reason_for_vardb_class"] = reason_for_vardb_class
        self["effect"] = effect
        self["bic"] = bic
        self["hgmd_pro"] = hgmd_pro
        self["sift"] = sift
        self["mutation_taster"] = mutation_taster
        self.is_changed = False
    def __del__(self):
        if self.is_changed:
            print "%s %d is changed" % (type(self), self["id"])

        
class Details(DeclarativeBase):
    __tablename__ = "details"
    
    id = Column(Integer, primary_key=True)
    gene = Column("gene", String(20))
    hgvs_cdna = Column("hgvs_cdna", String(20))
    observed_genotype = Column("observed_genotype", String(20))
    reason_for_vardb_class = Column("reason_for_vardb_class", String(200))
    effect = Column("effect", String(50))
    bic = Column("bic", String(50))
    hgmd_pro = Column("hgmd_pro", String(50))
    sift = Column("sift", String(50))
    mutation_taster = Column("mutation_taster", String(50))
    
          
metadata.create_all()
