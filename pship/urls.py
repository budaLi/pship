"""pship URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^hangcheng/(\d+)/$', views.hangcheng,name="hangcheng"),
    url(r'^select_pship/$', views.select_pship,name="select_pship"),
    # url(r'^show_ship/', views.show_ship,name="show_ship"),
    url(r'^hangcheng_del/(\d+)/$', views.hangcheng_del,name="hangcheng_del"),
    url(r'^hangcheng_edit/(\d+)/$', views.hangcheng_edit,name="hangcheng_edit"),
     url(r'^pship_list/', views.pship_list,name='pship_list'),
    url(r'^pship_add/', views.pship_add,name='pship_add'),
    url(r'^pship_edit/(\d+)/$', views.pship_edit,name='pship_edit'),
    url(r'^pship_del/(\d+)/$', views.pship_del,name='pship_del'),
    url(r'^pport_add/(\d+)$', views.pport_add,name='pport_add'),
    url(r'^pport_edit/(\d+)/$', views.pport_edit,name='pport_edit'),
    url(r'^pport_del/(\d+)/$', views.pport_del,name='pport_del'),
    url(r'^cost_budget/(\d+)/$', views.cost_budget,name='cost_budget'),
    url(r'^budgetresult_del/(\d+)/$', views.budgetresult_del,name='budgetresult_del'),
    url(r'^cost_budget_selectship/$', views.cost_budget_selectship,name='cost_budget_selectship'),
    url(r'^total_budget_selectship/$', views.total_budget_selectship,name='total_budget_selectship'),
    url(r'^cost_del/(\d+)/$', views.cost_del,name="cost_del"),
    url(r'^cost/(\d+)/$', views.cost,name="cost"),
    url(r'^fuelrent_add/(\d+)/$', views.fuelrent_add,name="fuelrent_add"),
    url(r'^fuelrent_edit/(\d+)/$', views.fuelrent_edit,name="fuelrent_edit"),
    url(r'^fuelrent_del/(\d+)/$', views.fuelrent_delete,name="fuelrent_delete"),
    url(r'^pcargo_add/(\d+)/$', views.pcargo_add,name="pcargo_add"),
    url(r'^pcargo_edit/(\d+)/$', views.pcargo_edit,name="pcargo_edit"),
    url(r'^pcargo_del/(\d+)/$', views.pcargo_del,name="pcargo_del"),
    url(r'^pport_order/(\d+)/$', views.Get_pport_order,name="pport_order"),
    url(r'^budget_result/(\d*)$', views.budget_result,name="budget_result"),
    url(r'^$', views.index,name="index"),
    url(r'^all_info/$', views.all_info,name="all_info"),
]
