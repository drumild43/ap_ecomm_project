from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Product
from .models import EcomUser, Cart

def home(request, user_id=None):
    if user_id:
        curr_user = EcomUser.objects.get(pk=user_id)
        context = {'curr_user': curr_user}
    else:
        context = {}
    return render(request, 'store/homepage.html', context=context)

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
            new_cart = Cart()

            new_user = EcomUser(
                first_name=first_name, 
                last_name=last_name, 
                email=email, 
                address=address,
                cart = new_cart,
                logged_in = True
            )
            new_cart.save()
            new_user.set_password(password1)
            new_user.save()

            return HttpResponseRedirect(reverse('store:homepage', args=(new_user.id,)))

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
            return HttpResponseRedirect(reverse('store:homepage', args=(ecomuser.id,)))

        else:
            return render(request, 'store/signin.html', context={'error_message': "Incorrect password."})

def logout(request, user_id):
    if request.method == 'POST':
        curr_user = EcomUser.objects.get(pk=user_id)
        curr_user.logged_in = False
        curr_user.save()

    return HttpResponseRedirect(reverse('store:anon_homepage'))

def products(request):
    products = Product.objects.all()
    srch_prods = []
    filter_prods = []

    if request.method == 'GET':
        srch = request.GET.get('inputbar')
        cat_sports = request.GET.get('cat_sports')
        cat_formal = request.GET.get('cat_formal')
        cat_flipflops = request.GET.get('cat_flipflops')
        cat_casual = request.GET.get('cat_casual')
        sort_HtoL = request.GET.get('sort_H_to_L')
        sort_LtoH = request.GET.get('sort_L_to_H')
        if srch:
            for product in products:
                if srch in product.name.lower() or srch in product.description.lower() or srch in product.category.lower():
                    srch_prods += product

            products = []
            products += srch_prods    

            if products == []:
                errormessage = 'No match for your search'
                context = {'products': products, 'errormessage': errormessage}
            else:
                context = {'products': products}
            return render(request, 'store/product.html', context)

        if sort_HtoL:
            if cat_sports:
                filter_prods += Product.objects.filter(category__name = cat_sports)
            
            if cat_formal:
                filter_prods += Product.objects.filter(category__name = cat_formal)

            if cat_flipflops:
                filter_prods += Product.objects.filter(category__name = cat_flipflops)

            if cat_casual:
                filter_prods += Product.objects.filter(category__name = cat_casual)
                
            if filter_prods == []:
                filter_prods += Product.objects.order_by('-price')
                products = []
                products += filter_prods
                context = {'products': products}
                return render(request, 'store/product.html', context)
            
            products = []
            products += filter_prods
            context = {'products': products}

            return render(request, 'store/product.html', context)

        if sort_LtoH:
            if cat_sports:
                filter_prods += Product.objects.filter(category__name = cat_sports)
            
            if cat_formal:
                filter_prods += Product.objects.filter(category__name = cat_formal)

            if cat_flipflops:
                filter_prods += Product.objects.filter(category__name = cat_flipflops)

            if cat_casual:
                filter_prods += Product.objects.filter(category__name = cat_casual)
            
            if filter_prods == []:
                filter_prods += Product.objects.order_by('price')
                products = []
                products += filter_prods
                context = {'products': products}
                return render(request, 'store/product.html', context)

            #not sure how to sort after filtering

            products = []
            products += filter_prods
            context = {'products': products}

            return render(request, 'store/product.html', context)

        if cat_sports:
            filter_prods += Product.objects.filter(category__name = cat_sports)
            
        if cat_formal:
            filter_prods += Product.objects.filter(category__name = cat_formal)

        if cat_flipflops:
            filter_prods += Product.objects.filter(category__name = cat_flipflops)

        if cat_casual:
            filter_prods += Product.objects.filter(category__name = cat_casual)

        products = []
        products += filter_prods
        context = {'products': products}
        return render(request, 'store/product.html', context)

    all_prods = 'All products'            
    context = {'products': products, 'all_prods': all_prods}
    return render(request, 'store/product.html', context)


def account(request, user_id):
    curr_user = EcomUser.objects.get(pk=user_id)
    return render(request, 'store/account.html', context={'curr_user': curr_user})

def pers_details(request, user_id):
    curr_user = EcomUser.objects.get(pk=user_id)

    if request.method == 'GET':
        return render(request, 'store/pers-details.html', context={'curr_user': curr_user})

    if request.method == 'POST':
        curr_password = request.POST['curr_password'].strip()
        new_first_name = request.POST.get('first_name')
        new_last_name = request.POST.get('last_name')
        new_password = request.POST.get('new_password')

        if curr_user.check_password(curr_password):
            if new_first_name:
                curr_user.first_name = new_first_name

            if new_last_name:
                curr_user.last_name = new_last_name

            if new_password:
                curr_user.set_password(new_password)

            curr_user.save()

            return HttpResponseRedirect(reverse('store:account', args=(user_id,)))

        # if current password entered is wrong
        else:
            context = {
                'curr_user': curr_user,
                'new_first_name': new_first_name,
                'new_last_name': new_last_name,
                'error_message': "The current password you have entered is incorrect."
            }
            return render(request, 'store/pers-details.html', context=context)

def address(request, user_id):
    curr_user = EcomUser.objects.get(pk=user_id)

    if request.method == 'GET':
        return render(request, 'store/address.html', context={'curr_user': curr_user})

    if request.method == 'POST':
        new_address = request.POST['address']
        # if new_address is not "", update address
        if new_address:
            curr_user.address = new_address
            curr_user.save()

        return HttpResponseRedirect(reverse('store:account', args=(user_id,)))