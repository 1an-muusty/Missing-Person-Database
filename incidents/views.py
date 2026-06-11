from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, MissingPersonForm
from django.contrib.auth.decorators import login_required
from .models import Missingperson
from django.db.models import Q


def home(request):
    return render(request, 'index.html')

def login_users(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have logged in succesfully')
            return redirect('home')
        else:
            messages.error(request, 'Error while logging in. Please Try again')
            return redirect('login')
    else:
        return render(request, 'login.html', {})
    
def logout_users(request): 
    logout(request)
    messages.success(request, 'You are successfully logged out')
    return redirect('home')

def register_users(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            #login user
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, 'You have registered succesfully')
            return redirect('home')
        else:
            messages.error(request, 'There was a problem while registering, Please try again')
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})
    

@login_required
def report_missing_person(request):
    if request.method == 'POST':
        form = MissingPersonForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)  # Ensure `lastSeenDate` is parsed correctly
            missing_person = form.save(commit=False)
            missing_person.user = request.user  
            missing_person.save()
            messages.success(request, "Form submitted successfully")
            return redirect('view_missing_persons')  # Redirect to a relevant page after success
        else:
            messages.error(request, "There was an error with the form submission. Please try again.")
            redirect('home')
    else:
        form = MissingPersonForm()  # Ensure `form` is initialized for GET requests

    return render(request, 'report_missing_person_form.html', {'form': form})


def view_missing_persons(request):
    # Get all missing persons by default
    missing_persons = Missingperson.objects.all()
    return render(request, 'view_database.html', {'missing_persons': missing_persons})

def missing_person_detail(request, id):
    missing_person = get_object_or_404(Missingperson, id=id)
    return render(request, 'missing_person_detail.html', {'missing_person': missing_person})

@login_required
def user_dashboard(request):
    reports = Missingperson.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'reports': reports})

@login_required
def edit_report(request, report_id):
    report = get_object_or_404(Missingperson, id=report_id, user=request.user)
    if request.method == 'POST':
        form = MissingPersonForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')
    else:
        form = MissingPersonForm(instance=report)
    return render(request, 'edit_report.html', {'form': form})

@login_required
def delete_report(request, report_id):
    report = get_object_or_404(Missingperson, id=report_id, user=request.user)
    if request.method == 'POST':
        report.delete()
        return redirect('user_dashboard')
    return render(request, 'delete_report.html', {'report': report})

def login_required_message(request):
    return render(request, 'login_required.html')

def search(request):
    query = request.GET.get('query', '')  
    location = request.GET.get('location', '')  
    # Start with all missing persons as the default
    results = Missingperson.objects.all()

    # Filter by query (first name or last name)
    if query:
        results = results.filter(Q(fname__icontains=query) | Q(lname__icontains=query))

    # If location is provided, filter by location as well
    if location:
        results = results.filter(lastSeenLocation__icontains=location)

    # Render the results to the same template (view_database.html)
    return render(request, 'view_database.html', {
        'results': results,
        'query': query,
        'location': location,
    })


