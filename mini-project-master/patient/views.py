from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
import MySQLdb
import mysql.connector
from django import forms
from importlib import import_module
from django.conf import settings
from accounts.views import login
import getpass


# Create your views here.

def patient(request):
    conn = mysql.connector.connect(user = 'root',password = 'root',host = 'localhost',database = 'trial')
    mycursor = conn.cursor()
    usrn = request.session["user"]
    u_name = request.session['uid']
    query = "select usrname from person where id = '" + str(u_name) + "'"
    mycursor.execute(query,())
    pt_name = mycursor.fetchone()
    return render(request,'patient/patient.html',{'pt_name':pt_name[0]})    

def appointment(request):
    conn = mysql.connector.connect(user = 'root',password = 'root',host = 'localhost',database = 'trial')
    mycursor = conn.cursor()
    q = "select usrname from person where prof='Doctor' "
    mycursor.execute(q,())
    res = mycursor.fetchall()    
    if request.method == 'POST':
        usrname = request.POST['usrname']
        doctor = request.POST['doctor']
        gen = request.POST['gender']
        phno = request.POST['phno']
        emailid = request.POST['emailid']
        date = request.POST['dt']
        time = request.POST['time']

        query1 = 'insert into appoint values (a_id,(select id from person where emailid="'+emailid+'"),"' + usrname + '",(select emailid from person where usrname = "'+doctor +'"),"' + gen + '","' + phno + '","' + emailid + '","' + date + '","' + time + '")'
        mycursor.execute(query1,())
        
        conn.commit()
        conn.close()
        
        return redirect('/patient')
    else:
        return render(request,'patient/appointment.html',{'result':res})


def bill(request):
    conn = mysql.connector.connect(user = 'root',password = 'root',host = 'localhost',database = 'trial')
    mycursor = conn.cursor()
    usrn = request.session["user"]
    u_id = request.session["uid"]
    query1 = "select phno,emailid,usrname from person where emailid = '" + request.session["user"] + "'"
    query2 = "select bill_id,doc_name,bill_dt,diag,amt,total_amt from bill where id = '" + str(u_id) + "'"
    
    mycursor.execute(query1,())
    res1=mycursor.fetchall()
    
    mycursor.execute(query2,())
    res2=mycursor.fetchall()
    
    conn.commit()
    conn.close()
    return render(request,'patient/bill.html',{'usrname':res1[0][2],'phno': res1[0][0],'emailid': res1[0][1],'date':res2[0][2],'bill_id':res2[0][0],'doc':res2[0][1],'diag':res2[0][3],'amt':res2[0][4],'tot':res2[0][5]})    


def p_logout(request):
    #conn = mysql.connector.connect(user = 'root',password = 'root',host = 'localhost',database = 'trial')
    #mycursor = conn.cursor()
    #query1="update person set status='F' where status='T' "
    #mycursor.execute(query1,())
    #conn.commit()
    #conn.close()
    request.session.flush()
    return redirect('/')

def del_bill(request):
    conn = mysql.connector.connect(user = 'root',password = 'root',host = 'localhost',database = 'trial')
    mycursor = conn.cursor()
    
    u_id=request.session["uid"]
    #query2= "delete from bill where bill_dt in (select min(bill_dt) from bill where id= '" + str(u_id) + "' ) "
    #res3=mycursor.fetchall()
    query2 = " delete from bill where id = '" + str(u_id) + "' " 
    mycursor.execute(query2,())
    conn.commit()
    conn.close()
    return render(request,'patient/patient.html')

def view_bills(request):
    conn = mysql.connector.connect(user = 'root',password = 'root',host = 'localhost',database = 'trial')
    mycursor = conn.cursor()
    uid=request.session["uid"]
    
    query1="select bill_id,bill_dt from bill where id='"+str(uid)+"'"
    mycursor.execute(query1,())
    res=mycursor.fetchall()
    query2="select bill_id from bill where id='"+str(uid)+"'"
    mycursor.execute(query2)
    res1=mycursor.fetchall()
    request.session["bills"]=res1
    conn.commit()
    conn.close()
    return render(request,'patient/view_bills.html',{'result':res})