from django.shortcuts import render, redirect
from .models import Document
from .forms import DocumentForm, CreateUserForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import mimetypes
import os
from django.contrib import messages
from django.conf import settings  # Import settings to access MEDIA_ROOT
from rest_framework import viewsets
from .models import Document
from .serializers import DocumentSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required




def Register(request):
    form = CreateUserForm()
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('home') 
        else:
            messages.error(request, 'Please correct the errors below.')

    context = {'form': form}
    return render(request, "register.html", context)

def Login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Log in the user
            return redirect('home')  # Redirect to the home page
        else:
            messages.error(request, 'Invalid username or password.')
            
    
    context = {}
    return render(request, "login.html", context)

def Logout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('login')

@login_required(login_url='login')
def home(request):
    documents = Document.objects.all()
    
    if request.method == 'POST':
        if 'upload' in request.POST:  # Check if the form is for uploading
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Document uploaded successfully.')
                return redirect('home')
        elif 'delete' in request.POST:  # Check if the form is for deleting
            document_id = request.POST.get('document_id')
            document = get_object_or_404(Document, id=document_id)
            # Delete the file from the media/documents directory
            file_path = document.file.path
            if os.path.exists(file_path):
                os.remove(file_path)  # Delete the file from the file system
            document.delete()  # Delete the document record from the database
            messages.success(request, 'Document deleted successfully.')
            return redirect('home')
        elif 'update' in request.POST:  # Check if the form is for updating
            document_id = request.POST.get('document_id')
            document = get_object_or_404(Document, id=document_id)
            form = DocumentForm(request.POST, request.FILES, instance=document)
            if form.is_valid():
                form.save()
                messages.success(request, 'Document updated successfully.')
                return redirect('home')
    else:
        form = DocumentForm()

    return render(request, "index.html", {'documents': documents, 'form': form})


@login_required(login_url='login')
def document_download(request, document_id):
    document = get_object_or_404(Document, id=document_id)

    # Get the file's full path
    file_path = document.file.path

    # Guess the content type based on the file extension
    content_type, _ = mimetypes.guess_type(file_path)

    # Set the default content type if it can't be guessed
    if content_type is None:
        content_type = 'application/octet-stream'

    # Create the response
    response = HttpResponse(open(file_path, 'rb'), content_type=content_type)
    
    # Set the Content-Disposition header with the correct filename
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
    return response

class DocumentViewSet(viewsets.ModelViewSet):
    
    queryset = Document.objects.all()  # Fetch all documents
    serializer_class = DocumentSerializer

    
    
    





