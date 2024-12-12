from django.urls import path
from .views import home, document_download
from . import views

urlpatterns = [
    path('', home, name='home'),  # Home view
    path('download/<int:document_id>/', document_download, name='document_download'),  # Download view
    path('register/', views.Register, name='register'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
]
