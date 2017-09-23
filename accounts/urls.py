from django.conf.urls import url
from accounts import views

urlpatterns = [
    url(r'^login/', views.LoginView.as_view()),
    url(r'^profile/', views.ProfileView.as_view()),
]
