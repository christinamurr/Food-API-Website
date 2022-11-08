from django.urls import re_path, path
from app import views
from .API.YelpAPI.yelp import yelp_main, query_api

# SET THE NAMESPACE!
app_name = 'app'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    re_path('yelp_main/', yelp_main, name='yelp_main' ),
    path('query_api/', query_api, name='query_api'),
    path('registration/', views.register_request, name='registration'),
    re_path(r'^user_login/$', views.user_login,name='user_login'),
]
