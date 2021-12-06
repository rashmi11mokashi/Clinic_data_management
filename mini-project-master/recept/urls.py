from django.urls import path
from . import views
from django.conf.urls import url
import accounts.urls,accounts.views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('',views.index_recept,name="index_recept"),
    path('bill_final',views.bill_final,name="bill_final"),
    path('view_appoint',views.view_appoint,name="view_appoint"),
    #path('del_success',views.del_success,name="del_success"),
    path('show_bill',views.show_bill,name="show_bill"),
]

urlpatterns += staticfiles_urlpatterns()