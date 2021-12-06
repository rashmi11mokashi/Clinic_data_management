from django.shortcuts import render,redirect,render_to_response
from django.contrib.auth import logout
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User,auth
import MySQLdb
import mysql.connector
from django import forms
from importlib import import_module
from django.conf import settings
from django.contrib import messages 
from django.template.loader import render_to_string
from django.template import RequestContext

# Create your views here.

def doctor(request):
    conn = mysql.connector.connect(user = 'root',password = 'root',host = 'localhost',database = 'trial')
    mycursor = conn.cursor()
    uid = request.session["uid"]
    query1 = "select timing from doctor where id = '" + str(uid) +"'"
    mycursor.execute(query1,())
    time = mycursor.fetchone()
    return render(request,'doctor/doctor.html',{'time':time[0]})   

def d_bill(request):
    conn = mysql.connector.connect(user = 'root',password = 'root',host = 'localhost',database = 'trial')
    mycursor = conn.cursor()
    if request.method == 'POST':
        pusr = request.POST['usrname']
        diag = request.POST['diag']
        usrn = request.session["user"]
        query="select prof from person where usrname='"+pusr+"'"
        mycursor.execute(query,())
        res=mycursor.fetchone()
        if res[0]=='Patient':
            query1 = "insert into bill(id,doc_name,bill_dt,diag) values ((select id from person where usrname='"+pusr+"'),'"+ str(usrn) +"',(select CURDATE()),'"+ diag +"')"        
            mycursor.execute(query1,())
            conn.commit()
            conn.close()
            return redirect('/doctor')
        else:
            return render(request,'doctor/u_bill.html',{'result':-1})
    return render(request,'doctor/u_bill.html')     

def s_hours(request):
    conn = mysql.connector.connect(user = 'root',password = 'root',host = 'localhost',database = 'trial')
    mycursor = conn.cursor()
    if request.method == 'POST':
        # doc_id = request.session['user']
        # query="select usrname from person p,doctor d where '" + doc_id +"'=d.id"
        # mycursor.execute(query)
        # result=mycursor.fetchone()
        newtime = request.POST['time']
        # query1 = "update doctor set timing = '"+ newtime +"' where id in (select id from person where usrname='"+ result[0] +"')"
        # print(result[0])
        # mycursor.execute(query1)
        uid = request.session["uid"]
        query = " update doctor set timing = '"+ newtime +"' where id = '" + str(uid) +"' "
        mycursor.execute(query,())
        conn.commit()
        conn.close()
        return redirect('/doctor')
    else:
        return render(request,'doctor/s_hours.html')


def treat_list(request):
    conn = mysql.connector.connect(user = 'root',password = 'root',host = 'localhost',database = 'trial')
    mycursor = conn.cursor()
    usrn = request.session["user"]
    u_id = request.session["uid"]
    # query1 = "select usrname from person where emailid="+str(usrn)+" "
    # mycursor.execute(query1,())
    # res1=mycursor.fetchone()
    #query2 = "select d.id,d.usrname,d.emailid,d.phno,p.ht,p.wt,p.med_history from person d,patient p,appoint a where d.id=a.id and a.doctor="+res1[0]+""
    query2 = "select id,usrname from appoint where doctor ='"+ str(usrn) +"' "
    mycursor.execute(query2,())    
    res2=mycursor.fetchall()

    query3 = "select id,emailid,phno from person "
    mycursor.execute(query3,())    
    res3=mycursor.fetchall()

    query4 = "select id,ht,wt,med_history from patient"
    mycursor.execute(query4,())    
    res4=mycursor.fetchall()
    conn.commit()
    conn.close() 
    return render(request,'doctor/treat_list.html',{'res2':res2,'res3':res3,'res4':res4})     

def register(request):
    conn = mysql.connector.connect(user = 'root',password = 'root',host = 'localhost',database = 'trial')
    mycursor = conn.cursor()
    if request.method == 'POST':
        usrname = request.POST['usrn']
        addr = request.POST['addr']
        emailid = request.POST['email']
        id_p = int(request.POST['id_proof'])
        gen = request.POST['gender']
        dob = request.POST['dob']
        phno = int(request.POST['phno'])
        pswd1 = request.POST['pswd1']
        pswd2 = request.POST['pswd2']
        wh_hr = request.POST['wh_hr']
        sal = request.POST['sal']
        recep_type = request.POST['recep']

        query = 'insert into person(id,prof,usrname,addr,emailid,id_p,gender,dob,phno,pswd1,pswd2) values (id,"Receptionist","' + usrname + '","' + addr + '","' + emailid + '",' + str(id_p) + ',"' + gen + '","'+ dob + '",' + str(phno)+',"' + pswd1 + '","'+ pswd2 + '")'
        mycursor.execute(query,())
        query = 'insert into recept(id,r_salary,r_whrs,recep_name) values((select id from person where id_p='+str(id_p)+'),'+ str(sal) + ','+ str(wh_hr) +',"'+recep_type+'")'
        mycursor.execute(query,())
        conn.commit()
        conn.close()
        #equest.session["email"] = emailid
        #request.session["usr"] = usrname
        return redirect('/doctor')
    else:
        return render(request,'doctor/recep_reg.html') 

def d_logout(request):
    request.session.flush()
    return redirect('/')

def about(request):
    return render(request,'about.html')

def blog_home(request):
    return render(request,'blog-home.html')

def blog_single(request):
    return render(request,'blog-single.html')