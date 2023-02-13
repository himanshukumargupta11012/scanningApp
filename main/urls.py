from . import views
from django.urls import path


urlpatterns=[
  path('',views.home),
  path('signup',views.signup),
  path('signin',views.signin),
  path('logout',views.logout),
  path('verifyOtp',views.verifyOtp),
]