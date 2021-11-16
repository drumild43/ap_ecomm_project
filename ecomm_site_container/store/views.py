from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import EcomUser, Cart, CartItem, Order, OrderItem, Product, Wishlist, WishlistItem

def home(request, user_id=None):
    if user_id:
        curr_user = EcomUser.objects.get(pk=user_id)
        context = {'curr_user': curr_user}
    else:
        context = {}
    return render(request, 'store/homepage.html', context=context)

def signup(request, product_id=None):
    if request.method == 'GET':
        return render(request, 'store/signup.html', context={'product_id': product_id})

    elif request.method == 'POST':
        first_name = request.POST['first_name'].strip()
        last_name = request.POST['last_name'].strip()
        email = request.POST['email'].strip()
        password1 = request.POST['password1'].strip()
        password2 = request.POST['password2'].strip()
        address = request.POST['address']
        # if user already exists, prompt to sign in
        if list(EcomUser.objects.filter(email=email)):
            context = {'already_exists': True, 'product_id': product_id}
            return render(request, 'store/signup.html', context=context)

        # else, create new user if passwords match
        elif password1 == password2:
            new_cart = Cart()
            new_wishlist = Wishlist()

            new_user = EcomUser(
                first_name=first_name, 
                last_name=last_name, 
                email=email, 
                address=address,
                cart = new_cart,
                wishlist = new_wishlist,
                logged_in = True
            )
            new_cart.save()
            new_wishlist.save()
            new_user.set_password(password1)
            new_user.save()

            if product_id:
                return HttpResponseRedirect(
                    reverse('store:product-details', args=(new_user.id, product_id))
                )
            else:
                return HttpResponseRedirect(reverse('store:homepage', args=(new_user.id,)))

        # else prompt that passwords do not match
        else:
            context = {
                'error_message': "Passwords do not match.",
                'product_id': product_id,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'address': address
            }
            return render(request, 'store/signup.html', context=context)


def signin(request, product_id=None):
    context={'product_id': product_id}

    if request.method == 'GET':
        return render(request, 'store/signin.html', context=context)

    elif request.method == 'POST':
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()

        try:
            ecomuser = EcomUser.objects.get(email=email)
        except EcomUser.DoesNotExist:
            context['error_message'] = "No account with this email id exists."
            return render(request, 'store/signin.html', context=context)

        # if correct password
        if ecomuser.check_password(password):
            ecomuser.logged_in = True
            ecomuser.save()

            if product_id:
                return HttpResponseRedirect(
                    reverse('store:product-details', args=(ecomuser.id, product_id))
                )
            else:
                return HttpResponseRedirect(reverse('store:homepage', args=(ecomuser.id,)))
        # incorrect password
        else:
            context['error_message'] = "Incorrect password."
            return render(request, 'store/signin.html', context=context)

def logout(request, user_id):
    if request.method == 'POST':
        curr_user = EcomUser.objects.get(pk=user_id)
        curr_user.logged_in = False
        curr_user.save()

    return HttpResponseRedirect(reverse('store:anon_homepage'))

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

def product_details(request, product_id, user_id=None):
    product = Product.objects.get(id = product_id)
    context = {'product': product}

    if user_id:
        curr_user = EcomUser.objects.get(pk=user_id)
        context['curr_user'] = curr_user

    return render(request, 'store/product-details.html', context)

def cart(request, user_id, product_id=None, cartitem_id=None):
    curr_user = EcomUser.objects.get(pk=user_id)
    cart = curr_user.cart

    if request.method == 'GET':
        cart_subtotal = 0
        for cartitem in cart.cartitem_set.all():
            cart_subtotal += cartitem.quantity * (cartitem.product.price)

        context={'curr_user': curr_user, 'cart': cart, 'cart_subtotal': cart_subtotal}
        return render(request, 'store/cart.html', context=context)

    if request.method == 'POST':
        update_method = request.POST['update-method']

        # if add from product-details page
        if update_method == "add":
            item_quantity = int(request.POST['quantity'])
            item_size = int(request.POST['size'])
            cartitem_list = list(CartItem.objects.filter(
                product__pk=product_id,
                size=item_size,
                cart__pk=cart.id
            ))

            # if cartitem already exists
            if cartitem_list:
                cartitem = cartitem_list[0]
                cartitem.quantity += item_quantity
            # else, create cartitem
            else:
                cartitem = CartItem(
                    cart = cart,
                    product = Product.objects.get(pk=product_id),
                    quantity = item_quantity,
                    size = item_size
                )
            
            cart.total_quantity += item_quantity
            cart.save()
            cartitem.save()

        # if remove-all from cart page
        if update_method == "remove-all":
            CartItem.objects.filter(cart__pk=cart.id).delete()
            cart.total_quantity = 0
            cart.save()
            
        # if updates to specific cartitems from cart page
        else:
            cartitem = CartItem.objects.get(pk=cartitem_id)

            if update_method == "decrease":
                cartitem.quantity -= 1
                cart.total_quantity -= 1

            if update_method == "increase":
                cartitem.quantity += 1
                cart.total_quantity += 1
            
            cartitem.save()

            if update_method == "remove" or cartitem.quantity == 0:
                cart.total_quantity -= cartitem.quantity
                cartitem.delete()

            if update_method == "move-to-wl":
                cart.total_quantity -= cartitem.quantity
                
                wlitem_list = list(WishlistItem.objects.filter(
                    product__pk=cartitem.product.id,
                    wishlist__pk=curr_user.wishlist.id
                ))

                # create item only if not in wishlist already
                if not wlitem_list:
                    wlitem = WishlistItem(
                        wishlist=wishlist, 
                        product=Product.objects.get(pk=product_id)
                    )
                    wlitem.save()

                cartitem.delete()

            cart.save()

        return HttpResponseRedirect(reverse('store:cart', args=(user_id,)))

def wishlist(request, user_id, product_id=None):
    curr_user = EcomUser.objects.get(pk=user_id)
    wishlist = curr_user.wishlist

    if request.method == 'GET':
        context = {'curr_user': curr_user, 'wishlist': wishlist}
        return render(request, 'store/wishlist.html', context=context)

    if request.method == 'POST':
        update_method = request.POST['update-method']

        # move from cart to wishlist is implemented in cart view

        # if add from product-details page
        if update_method == "add":
            wlitem_list = list(WishlistItem.objects.filter(
                product__pk=product_id,
                wishlist__pk=wishlist.id
            ))
            
            # create item only if not in wishlist already
            if not wlitem_list:
                wlitem = WishlistItem(
                    wishlist=wishlist, 
                    product=Product.objects.get(pk=product_id)
                )
                wlitem.save()
            
            return HttpResponseRedirect(reverse('store:wishlist', args=(user_id,)))

        # if remove from wishlist page
        if update_method == "remove":
            WishlistItem.objects.filter(product__pk=product_id).delete()

        # if remove-all from wishlist page
        if update_method == "remove-all":
            WishlistItem.objects.filter(wishlist__pk=wishlist.id).delete()

        return HttpResponseRedirect(reverse('store:wishlist', args=(user_id,)))

def checkout(request, user_id):
    curr_user = EcomUser.objects.get(pk=user_id)
    cart = curr_user.cart

    cart_subtotal = 0
    for cartitem in cart.cartitem_set.all():
        cart_subtotal += cartitem.quantity * (cartitem.product.price)

    if request.method == 'GET':
        context = {'curr_user': curr_user, 'cart': cart, 'cart_subtotal': cart_subtotal}
        return render(request, 'store/checkout.html', context=context)

    if request.method == 'POST':
        # create order
        order = Order(
            user=curr_user, 
            order_total=cart_subtotal, 
            total_quantity=cart.total_quantity
        )
        order.save()

        # add orderitems and remove corresponding cartitems
        for cartitem in cart.cartitem_set.all():
            orderitem = OrderItem(
                order=order,
                product=cartitem.product,
                quantity=cartitem.quantity,
                size=cartitem.size
            )
            orderitem.save()
            cartitem.delete()

        cart.total_quantity = 0
        return HttpResponseRedirect(reverse('store:pay-suc', args=(user_id,)))

def pay_suc(request, user_id):
    curr_user = EcomUser.objects.get(pk=user_id)
    return render(request, 'store/paysuc.html', context={'curr_user': curr_user})

def cancel_order(request, user_id, order_id):
    if request.method == 'POST':
        order = Order.objects.get(pk=order_id)
        order.status = 'X'
        
        return HttpResponseRedirect(reverse('store:account', args=(user_id,)))