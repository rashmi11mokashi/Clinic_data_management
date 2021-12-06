from django.urls import path
from . import views
from django.conf.urls import url
import accounts.urls,accounts.views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('',views.patient,name="patient"),
    path('appointment',views.appointment,name="appointment"),
    path('bill',views.bill,name="bill"),    
    path('logout',views.p_logout,name="logout"),
    path('del_bill',views.del_bill,name="del_bill"),
    path('view_bills',views.view_bills,name="view_bills"),

]

urlpatterns += staticfiles_urlpatterns()