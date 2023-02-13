from . import views
from django.urls import path


urlpatterns=[
  path('',views.home),
  path('/verifyPassword',views.verifyPassword),
  path('/logoutAdmin',views.logout),
]