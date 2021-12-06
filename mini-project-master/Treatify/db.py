from django.shortcuts import render

def fire_query(request):
    sql="desc doctor"
    return render(request,'db_con.py',{'que':sql})