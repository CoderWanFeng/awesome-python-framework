from django.urls import path,re_path
from . import views

urlpatterns = [
    path('',views.index_view),
    path('shoplist',views.shoplist_view),
    path('shopdetail/<int:_id>',views.shopdetail_view),
    path('login',views.login_view),
    path('manage/userinfo',views.manage_view),
    path('manage/myshop',views.myshop_view),
    path('manage/charge',views.charge_view),
    path('manage/rentshop',views.rent_view)
]