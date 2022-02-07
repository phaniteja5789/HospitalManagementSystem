from flask import Flask
from application import db
from werkzeug.security import generate_password_hash,check_password_hash

class login_casestudy(db.Document):
    
    username = db.StringField( max_length=30)
    password = db.StringField( max_length=30)

class Patient(db.Document):
    
    patientid = db.StringField(unique=True,max_length=9)
    patientname = db.StringField(max_length=30)
    patientage = db.StringField(max_length=3)
    patientdoj = db.StringField(max_length=30)
    patientbed = db.StringField(max_length=30)
    patientaddress = db.StringField(max_length=200)
    patientstate = db.StringField(max_length=30)
    patientcity = db.StringField(max_length=30)
    patientstatus=db.StringField(max_length=30)

class patient_medicines(db.Document):
    patientid=db.StringField(unique=True)
    MedicineID=db.ListField()
    quantityissued=db.ListField()

class pharma_medicines(db.Document):
    MedicineID=db.StringField(unique=True)
    Medicinename=db.StringField(max_length=50)
    rate=db.StringField(max_length=30)
    quantity=db.StringField(max_length=30)
class patient_diagnostics(db.Document):
    patientid=db.StringField(unique=True)
    testid=db.ListField(max_length=10)

class pharma_diagnostics(db.Document):
    testid=db.StringField(unique=True)
    testname=db.StringField(max_length=20)
    cost=db.StringField(max_length=10)
