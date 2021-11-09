from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import EcomUser

# Display Hello, userfullname if user logged in; implement on all pages !!!!!!!!!!

# incomplete!!!!
def home(request):
    return render(request, 'store/homepage.html', context={})

def signup(request):
    if request.method == 'GET':
        return render(request, 'store/signup.html', context={})

    elif request.method == 'POST':
        first_name = request.POST['first_name'].strip()
        last_name = request.POST['last_name'].strip()
        email = request.POST['email'].strip()
        password1 = request.POST['password1'].strip()
        password2 = request.POST['password2'].strip()
        address = request.POST['address']
        # if user already exists, prompt to sign in
        if list(EcomUser.objects.filter(email=email)):
            error_message = "An account with this email already exists. Please sign in instead."
            return render(request, 'store/signup.html', {'error_message': error_message})

        # else, create new user if passwords match
        elif password1 == password2:
            new_user = EcomUser(
                first_name=first_name, 
                last_name=last_name, 
                email=email, 
                address=address,
                logged_in = True
            )
            new_user.set_password(password1)
            new_user.save()

            return HttpResponseRedirect(reverse('store:homepage'))

        # else prompt that passwords do not match
        else:
            error_message = "Passwords do not match."
            context = {
                'error_message': error_message,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'address':address
            }
            return render(request, 'store/signup.html', context=context)


def signin(request):
    if request.method == 'GET':
        return render(request, 'store/signin.html', context={})

    elif request.method == 'POST':
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()

        try:
            ecomuser = EcomUser.objects.get(email=email)
        except EcomUser.DoesNotExist:
            return render(request, 'store/signin.html', context={'error_message': "No account with this email id exists."})

        if ecomuser.check_password(password):
            ecomuser.logged_in = True
            ecomuser.save()
            return HttpResponseRedirect(reverse('store:homepage'))
        else:
            return render(request, 'store/signin.html', context={'error_message': "Incorrect password."})

# def logout(request):