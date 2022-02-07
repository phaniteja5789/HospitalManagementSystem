from application import app,db
from flask import render_template,url_for,request, redirect, flash,session
from application.models import login_casestudy,Patient,patient_medicines,pharma_medicines,patient_diagnostics,pharma_diagnostics
from datetime import date
laptop=[]
laptop2=[]


@app.route('/',methods=['GET','POST'])
def index():
    if(request.method=='POST'):
        session["user"]=request.form.get('username')
        session["passw"]=request.form.get('password')
        l=login_casestudy.objects(username=session["user"],password=session["passw"]).first()
        
        try:
            
            if l:
                print("logged in Sucessfully")
                flash("logged in Sucessfully")
                return render_template('includes/base_header.html',login=True)
            else:
                raise ex
                
        except:
            print(" no User")
            flash("Authentication Failed")
            return redirect('/')    
    
    return render_template('includes/base_template.html',login=False)

@app.route('/patient',methods=['GET','POST'])
def patient():
    return render_template('includes/base_header.html',login=True)

@app.route('/createpatient',methods=['GET','POST'])
def createpatient():
    
    if(request.method=='POST'):
        session["patientid"]=request.form.get('patientssn')
        session["patientname"]=request.form.get('patientname')
        session["patientAge"]=request.form.get('patientAge')
        session["dateofadmission"]=request.form.get('dateofadmission')
        session["typeofbed"]=request.form.get('typeofbed')
        session["Address"]=request.form.get('Address')
        session["Address"]=session["Address"].strip()
        session["state"]=request.form.get('state')
        session["city"]=request.form.get('city')
        session["status"]="Active"
        l1=Patient.objects(patientid=session["patientid"]).first()
        
        
        try:
            if l1:
                raise ex
                
            else:
                l=Patient(patientid=session["patientid"],patientname=session["patientname"],patientage=session["patientAge"],patientdoj=session["dateofadmission"],patientbed=session['typeofbed'],patientaddress=session["Address"],patientstate=session["state"],patientcity=session["city"],patientstatus=session["status"])
                l.save()
                flash("Patient Registered Successfully")
                return render_template('includes/base_header.html',login=True)
                
        except:
            print("User exists")
            flash("User already exists")
            return redirect('/createpatient')    
        
    return render_template("includes/createpatient.html",login=True)


@app.route('/updatepatient' ,methods=['GET','POST'])
def updatepatient():
    p=None
    w=1
    if(request.method=='POST'):

        if("geta" in request.form):
            
            session["pidav"]=request.form.get('patientssn')
            p=Patient.objects(patientid=session["pidav"]).first()
            if p:

                return render_template("includes/updatepatient.html",p=p,w=w,login=True)
            else:
                print('no user')
                flash(" No Patient with given ID")
                return redirect('/updatepatient')
        
        else:
            w=0
            p=Patient.objects(patientid=session["pidav"]).first()
            if p:
                session["patientnamep"]=request.form.get('patientname')
                session["patientAgep"]=request.form.get('patientAge')
                session["dateofadmissionp"]=request.form.get('dateofadmission')
                session["typeofbedp"]=request.form.get('typeofbed')
                print(session["typeofbedp"])
                session["Addressp"]=request.form.get('Address')
                session["statep"]=request.form.get('state')
                session["cityp"]=request.form.get('city')
                if session["patientnamep"] is None:
                    print(session["patientnamep"],"if")
                    pass
                else:
                    
                    p.patientname=session["patientnamep"]
                if session["patientAgep"] is None:
                    
                    pass
                else:
                    print(session["patientAgep"],",else")
                    p.patientage=session["patientAgep"]
                if session["dateofadmissionp"] is None:
                    pass
                else:
                    p.patientdoj=session["dateofadmissionp"]
                
                if session["typeofbedp"] == "Select":
                    print(session["typeofbedp"],"if")
                    pass
                else:
                    print(session["typeofbedp"],"else")
                    p.patientbed=session["typeofbedp"]
                if session["Addressp"] is None:
                    pass
                else:
                    session["Addressp"]=session["Addressp"].strip()
                    p.patientaddress=session["Addressp"]
                if session["statep"] == "Select":
                    pass
                else:
                    p.patientstate=session["statep"]
                if session["cityp"] == "Select":
                    pass
                else:
                    p.patientcity=session["cityp"]
                p.save()
                print("Updated")
                flash("Patient detailes updated successfully")
                return render_template("includes/base_header.html",login=True)
            else:
                print('no user abc')
                flash("No Patient with given ID")
                return render_template('includes/updatepatient.html',login=True,w=w,p=p)
        
    return render_template("includes/updatepatient.html",login=True,w=w,p=p)

@app.route('/deletepatient',methods=['GET','POST'])
def deletepatient():
    p=None
    if(request.method=='POST'):
        if("geta" in request.form):
            session["pid"]=request.form.get('patientssn')
            p=Patient.objects(patientid=session["pid"]).first()
            if p:
                return render_template("includes/deletepatient.html",p=p,login=True)
            else:
                print('no user')
                flash("No Patient with given ID")
                return redirect('/deletepatient')
        else:
            p=Patient.objects(patientid=session["pid"]).first()
            if p:
                try:
                    
                    print("deleted")
                    flash("Deleted Suceessfully")
                    
                    Patient.objects(patientid=session["pid"]).delete()
                    
                    pap=patient_diagnostics.objects(patientid=session["pid"]).first()
                    
                    if pap:
                        patient_diagnostics.objects(patientid=session["pid"]).delete()
                        pap1=patient_medicines.objects(patientid=session["pid"]).first()
                        if pap1:
                            print(" patient_diagnostics, patient_medicines")
                            patient_medicines.objects(patientid=session["pid"]).delete()
                        else:
                            print("patient_diagnostics,no patient_medicines") 
                            raise ex
                    
                    else:
                        print("no patient_diagnostics")
                        pap1=patient_medicines.objects(patientid=session["pid"]).first()
                        if pap1:
                            print("no patient_diagnostics,patient_medicines")
                            patient_medicines.objects(patientid=session["pid"]).delete()
                        else:
                            print("no patient_diagnostics,no patient_medicines")
                            raise ex
                    
                        print("no patient_diagnostics")
                        raise ex
                    return render_template("includes/base_header.html",login=True)
                except:
                    print("User is not defined in all tables")
                    return render_template("includes/base_header.html",login=True)
            else:
                print('no user')
                flash("No Patient with given ID")
                return redirect('/deletepatient')
            

            
    return render_template("includes/deletepatient.html",login=True,p=p)

@app.route('/viewpatients')
def viewpatients():
    pa=Patient.objects.all()
    l=[]
    for x in pa:
        print( x.patientstatus)
        if x.patientstatus=='Active':
            print(l)
            l.append(x)
            print(l)        
    
    flash("Active Patients")
    return render_template("includes/viewpatients.html",l=l,login=True)

@app.route('/searchpatient',methods=['GET','POST'])
def searchpatient():
    p=None
    if(request.method=='POST'):
        session["pida"]=request.form.get('patientssn')
        p=Patient.objects(patientid=session["pida"]).first()
        if p:
            
            return render_template("includes/searchpatient.html",p=p,login=True)
        else:
            print('no user')
            flash("No Patient with given PatientID")
            return redirect('/searchpatient')
    
    return render_template("includes/searchpatient.html",login=True,p=p)

@app.route('/patientbilling',methods=['GET','POST'])
def patientbilling():
    sumpharma=0
    sumdia=0
    diff=0
    p=None
    m2=[]
    m3=[]
    m4=[]
    m=None
    l=0
    l1=0
    q=None
    q1=[]
    q2=[]
    delta=0
    date1=date.today()
    days=0
    rb=0
    total=0
    print(date1)
    if(request.method=='POST'):
        if ("se" in request.form):
            session["hms"]=request.form.get('opa')
            p=Patient.objects(patientid=session["hms"]).first()

            if p:
                if p.patientstatus=='Active':

                    m=patient_medicines.objects(patientid=session["hms"]).first()
                    if m:
                        m1=list(m.MedicineID)
                        m2=list(m.quantityissued)
                        l=len(m1)
                        i=0
                        date1=str(date1)
                        ldate1=date1.split('-')
                        ldate2=p.patientdoj.split('-')
                        f_date=date(int(ldate1[0]),int(ldate1[1]),int(ldate1[2]))
                        l_date=date(int(ldate2[0]),int(ldate2[1]),int(ldate2[2]))
                        delta=f_date-l_date
                        if (p.patientbed == "General Ward"):
                
                            rb=int(delta.days)*2000
                        elif (p.patientbed == "Semi Sharing"):
                
                            rb=int(delta.days)*4000
                        elif (p.patientbed == "Single room"):
                
                            rb=int(delta.days)*8000
                        else:
                            pass
            
            
                        for x in m1:
                            pw=pharma_medicines.objects(MedicineID=x).first()
                            m3.append(pw)
                            m4.append(int(pw.rate)*int(m2[i]))
                            sumpharma=sumpharma+int(pw.rate)*int(m2[i])
                            i=i+1
                        q=patient_diagnostics.objects(patientid=session["hms"]).first()
                        if q:
                            q1=list(q.testid)
                            l1=len(q1)
            
                            for x in q1:
                                pw1=pharma_diagnostics.objects(testid=x).first()
                                q2.append(pw1)
                                sumdia=sumdia+int(pw1.cost)
                            total=sumdia+sumpharma+rb
                            return render_template("includes/patientbilling.html",login=True,total=total,p=p,m=m,m3=m3,sumpharma=sumpharma,m2=m2,l=l,sumdia=sumdia,m4=m4,date1=date1,q2=q2,days=delta.days,rb=rb)
                        else:
                            total=sumdia+sumpharma+rb
                            print('No diagnostics')
                            flash("No Diagnostics for the Patient")
                            return render_template("includes/patientbilling.html",login=True,total=total,p=p,m=m,m3=m3,sumpharma=sumpharma,m2=m2,l=l,sumdia=sumdia,m4=m4,date1=date1,q2=q2,days=delta.days,rb=rb)
                    else:
                        print('No Medicines issued to the Patient')
                        flash("No medicines issued to the patient")
                        i=0
                        date1=str(date1)
                        ldate1=date1.split('-')
                        ldate2=p.patientdoj.split('-')
                        f_date=date(int(ldate1[0]),int(ldate1[1]),int(ldate1[2]))
                        l_date=date(int(ldate2[0]),int(ldate2[1]),int(ldate2[2]))
                        delta=f_date-l_date
                        if (p.patientbed == "General Ward"):
                
                            rb=int(delta.days)*2000
                        elif (p.patientbed == "Semi Sharing"):
                
                            rb=int(delta.days)*4000
                        elif (p.patientbed == "Single room"):
                
                            rb=int(delta.days)*8000
                        else:
                            pass
                        q=patient_diagnostics.objects(patientid=session["hms"]).first()
                        if q:
                            q1=list(q.testid)
                            l1=len(q1)
            
                            for x in q1:
                                pw1=pharma_diagnostics.objects(testid=x).first()
                                q2.append(pw1)
                                sumdia=sumdia+int(pw1.cost)
                            total=sumdia+sumpharma+rb
                            return render_template("includes/patientbilling.html",login=True,total=total,p=p,m=m,m3=m3,sumpharma=sumpharma,m2=m2,l=l,sumdia=sumdia,m4=m4,date1=date1,q2=q2,days=delta.days,rb=rb)
                        else:
                            print("No diagnostics else")
                            flash("No diagnostics and No Medicines")
                            total=sumdia+sumpharma+rb
                            return render_template("includes/patientbilling.html",login=True,total=total,p=p,m=m,m3=m3,sumpharma=sumpharma,m2=m2,l=l,sumdia=sumdia,m4=m4,date1=date1,q2=q2,days=delta.days,rb=rb)
                else:
                    print("Patient is already dischared")
                    flash("Patient Already discharged")
                    
                    return render_template("includes/patientbilling.html",login=True,total=total,p=p,m=m,m3=m3,sumpharma=sumpharma,m2=m2,l=l,sumdia=sumdia,m4=m4,date1=date1,q2=q2,days=delta,rb=rb)
                    
            else:
                print("No patient is found")
                flash("No Patient Found")
                total=sumdia+sumpharma+rb
                return render_template("includes/patientbilling.html",login=True,total=total,p=p,m=m,m2=m2,m3=m3,l=l,m4=m4,sumpharma=sumpharma,sumdia=sumdia,date1=date1,q2=q2,days=delta,rb=rb)
        else:
            p=Patient.objects(patientid=session["hms"]).first()
            p.patientstatus="Discharged"
            p.save()
            return render_template('includes/base_header.html',login=True)

    return render_template("includes/patientbilling.html",login=True,total=total,p=p,m=m,m2=m2,m3=m3,l=l,m4=m4,date1=date1,sumpharma=sumpharma,q2=q2,days=delta,rb=rb,sumdia=sumdia)

@app.route('/patientdetails',methods=['GET','POST'])
def patientdetails():
    p=None
    m=None
    a2=[]
    a4={}
    a5=[]
    l=0
    if(request.method=="POST"):
        session["po"]=request.form.get('pid')
        if( "se" in request.form):
            p=Patient.objects(patientid=session["po"]).first()
            if p:
                if p.patientstatus=="Active":

                #print(session["po"])
                    try:
                        m=patient_medicines.objects(patientid=session["po"]).first()
                        if m:
                            a1=list(m.MedicineID)
                            a5=list(m.quantityissued)
                #print(a1)
                            print(a5)
                            a2=[]
                            i=0
                            for x in a1:
                    
                                m2=pharma_medicines.objects(MedicineID=x).first()
                                if m2:
                                    print(m2.Medicinename)
                                    a2.append(m2)
                        
                                    a4[m2.Medicinename]=int(m2.rate)*int(a5[i])
                                i=i+1
                            return render_template("includes/patientdetails.html",p=p,a2=a2,a4=a4,a5=a5,l=len(a2),login=True)
                        else:
                            raise ex
                    except:
                        print("No medicines issued to the patient")
                        flash("No medicines issued to the patient")
                        return render_template("includes/patientdetails.html",p=p,a2=a2,a4=a4,a5=a5,l=len(a2),login=True)   
                else:
                    flash("Enter Patient Already Discharged")
                    return render_template("includes/patientdetails.html",p=p,a2=a2,a4=a4,a5=a5,l=len(a2),login=True)

            else:
                print("patient details not found")
                flash("patient details not found")
                return render_template("includes/patientdetails.html",p=p,a2=a2,a4=a4,a5=a5,l=len(a2),login=True)
        else:
            if(session["po"]):
                pt=Patient.objects(patientid=session["po"]).first()
                if pt:
                    if pt.patientstatus=="Active" :
                        return redirect('/issuemedicines')
                    else:
                        flash("Enter Patient Already Discharged")
                        return render_template("includes/patientdetails.html",p=p,a2=a2,a4=a4,a5=a5,l=len(a2),login=True)
                else:
                    flash("Patient ID invalid")
                    return render_template("includes/patientdetails.html",p=p,a2=a2,a4=a4,a5=a5,l=len(a2),login=True) 
            else:
                flash("Please Enter the Patient ID")
                return render_template("includes/patientdetails.html",p=p,a2=a2,a4=a4,a5=a5,l=len(a2),login=True)
                

    return render_template("includes/patientdetails.html",p=p,a2=a2,a4=a4,l=len(a2),login=True)

flag=0
@app.route('/issuemedicines',methods=['GET','POST'])
def issuemedicines():
    a=None
    d={}
    global laptop
    global flag
    
    if(request.method=='POST'):
        if( "sad" in request.form):
            session["abc1"]=request.form.get('abc1')
            session["abc2"]=request.form.get('abc2')
            flag=1  
            print(flag,"add")
            d['name']=session["abc1"]
            p1=pharma_medicines.objects(Medicinename=d['name']).first()
            d['quantity']=session["abc2"]
            
            if p1:
                
                if(int(p1.quantity)>=int(d['quantity'])):
                    
                    d['rate']=p1.rate
                    d['amount']=int(d['quantity'])*int(p1.rate)
                    laptop.append(d)
                   # print(laptop)
                    
                    return render_template("includes/issuemedicines.html",login=True,laptop=laptop)
                else:
                   # print('Required quantity is not there')
                    flash("Required quantity is not there")
                    
                    return render_template("includes/issuemedicines.html",login=True,laptop=laptop)                    
            else:
                print("no medicine")
                flash(" Medicine not available")
                return render_template("includes/issuemedicines.html",login=True,laptop=laptop)             
        else:
            print(flag)
            if flag==1:
                print(flag,"if")
                if laptop:
                    for m in laptop:
                        m1=pharma_medicines.objects(Medicinename=m['name']).first()
                        if m1:
                            m2=m1.MedicineID
                            m3=m['quantity']
                            p2=patient_medicines.objects(patientid=session["po"]).first()
                            if p2:
                                p2.quantityissued.append(m3)
                                p2.MedicineID.append(m2)
                                p2.save()
                                m1.quantity=int(m1.quantity)-int(m3)
                                m1.quantity=str(m1.quantity)
                                m1.save()
                                laptop=[]
                                print('Medicines issued succesfully')
                                flash("Medicines issued successfully")
                                return redirect('/patientdetails')
                            else:
                                patient_medicines(patientid=session["po"],MedicineID=[m2],quantityissued=[m3]).save()
                                if(len(laptop)==1):
                                    return redirect('/patientdetails')
                            
                        else:
                            print("No such medicine exists")
                            flash("No such medicine exists")
                            return render_template("includes/issuemedicines.html",login=True,laptop=laptop)
                else:
                    print('please enter medicines')
                    flash("Please enter medicines")
                    return render_template("includes/issuemedicines.html",login=True,laptop=laptop)                
            else:
                flash("Please Press Add Button Before Clicking on Update")
                
                return render_template("includes/issuemedicines.html",login=True,laptop=laptop)
    return render_template("includes/issuemedicines.html",login=True,laptop=laptop)

@app.route('/getpatientdetails',methods=['GET','POST'])
def getpatientdetails():
    p=None
    m=None
    a2=None
    a4={}
    if(request.method=="POST"):
        session["poa"]=request.form.get('pid')
        if( "se" in request.form):
            p=Patient.objects(patientid=session["poa"]).first()
            if p:
                try:

                #print(session["po"])
                    m=patient_diagnostics.objects(patientid=session["poa"]).first()
                    if m:
                        a1=list(m.testid)
                #print(a1)
                        a2=[]
                        for x in a1:

                            m2=pharma_diagnostics.objects(testid=x).first()
                            if m2:
                                print(m2.testname)
                                a2.append(m2)
                        
                                a4[m2.testname]=int(m2.cost)
                        return render_template("includes/getpatientdetails.html",p=p,a2=a2,a4=a4,login=True)
                    else:
                        raise ex
                except:
                    print("no tests for the patient")
                    flash("No tests conducted for the patient till now")
                    return render_template("includes/getpatientdetails.html",p=p,a2=a2,a4=a4,login=True)
            else:
                print("patient details not found")
                flash("Patient not found")
                return render_template("includes/getpatientdetails.html",p=p,a2=a2,a4=a4,login=True)
    
        else:
            if(session["poa"]):
                return redirect('/diagnostics')
            else:
                return render_template("includes/getpatientdetails.html",p=p,a2=a2,a4=a4,login=True)
           
    return render_template("includes/getpatientdetails.html",login=True,p=p,a2=a2,a4=a4)

@app.route('/diagnostics',methods=['GET','POST'])
def diagnostics():
    a=None
    d={}
    global laptop2
    if(request.method=='POST'):
        if( "sad" in request.form):
            session["abc1"]=request.form.get('ab1')
            d['name']=session["abc1"]
            p1=pharma_diagnostics.objects(testname=d['name']).first()
            if p1:
                d['cost']=int(p1.cost)
                laptop2.append(d)
                return render_template("includes/diagnostics.html",login=True,laptop2=laptop2)
            else:
                print("no test")
                flash("Entered test not available ")
                return render_template("includes/diagnostics.html",login=True,laptop2=laptop2)            
        else:
            
            if laptop2:
                for m in laptop2:
                    m1=pharma_diagnostics.objects(testname=m['name']).first()
                    if m1:
                        m2=m1.testid
                        p2=patient_diagnostics.objects(patientid=session["poa"]).first()
                        if p2:
                            p2.testid.append(m2)
                            p2.save()
                            laptop2=[]
                            print('Tests conducted suceesfully')
                            flash("Tests Conducted Sucessfully")
                            return redirect('/getpatientdetails')
                        else:
                            patient_diagnostics(patientid=session["poa"],testid=[m2]).save()
                            if(len(laptop2)==1):
                                return redirect('/getpatientdetails')
            else:
                print('please enter tests')
                flash("Please Enter the Tests")
                return render_template("includes/diagnostics.html",login=True,laptop2=laptop2)                

    return render_template("includes/diagnostics.html",login=True,laptop2=laptop2)
