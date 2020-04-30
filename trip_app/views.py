from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
from .models import Trip
import bcrypt

def index (request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.login_validator(request.POST)
    print(request.POST)
    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    print(pw_hash)
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = pw_hash)

        request.session['userid'] = user.id
        return redirect('/dashboard')
            
    return redirect('/')

def login(request):
        user = User.objects.filter(email = request.POST['email'])
        print(user)
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                return redirect('/dashboard')
            else:
                messages.error(request, "Email/password is incorrect.")
        else:
            messages.error(request, "Email isnt registered yet.")
        return redirect('/')

def dashboard(request):
    mytrips = User.objects.get(id = request.session['userid'])
    
    context ={
        'theuser' : mytrips,
        'trips':Trip.objects.filter(trip_details = mytrips),
    }
    return render(request, 'dashboard.html', context)

def create_trip(request):
    errors = Trip.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/trips/new')
    else:
        theuser = User.objects.get(id = request.session['userid'])
        #newtrip = Trip.objects.create(destination = request.POST["dest"], start_date = request.POST["start"], end_date = request.POST['end'], plan = request.POST['plan']) 
        
        Trip.objects.create(destination = request.POST["dest"], start_date = request.POST["start"], end_date = request.POST['end'], plan = request.POST['plan'],

        trip_details = theuser)
    return redirect('/dashboard')

def remove_trip(request, id):
    c = Trip.objects.get(id=id)
    c.delete()
    return redirect ('/dashboard')

def edit_trip(request, id):
    theuser = User.objects.get(id = request.session['userid'])
    context = {
        'edit_trip': Trip.objects.get(id=id),
        'theuser' : theuser
    }
    return render(request, 'edit.html', context)

def submit_edit(request, id):
    errors = Trip.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/edit_trip/{id}')
    else:
        c= Trip.objects.get(id=id)
        c.destination = request.POST['dest']
        c.start_date = request.POST['start']
        c.end_date = request.POST['end']
        c.plan = request.POST['plan']
        c.save()
        return redirect ('/dashboard')
    
def new_trip(request):
    context = {
    'theuser' : User.objects.get(id = request.session['userid'])
    }
    return render(request, 'new.html', context)
    

def see_trip(request, id):
    theuser = User.objects.get(id = request.session['userid'])
    context = {
        'edit_trip': Trip.objects.get(id=id),
        'theuser' : theuser,
        #'whomade' : Trip.objects.filter(trip_details = theuser)
    }
    return render(request, 'viewtrip.html', context)
def logout(request):
    request.session.clear()
    return redirect('/')