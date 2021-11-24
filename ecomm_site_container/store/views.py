from operator import attrgetter

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import EcomUser, Cart, CartItem, Order, OrderItem, Product, Review, Wishlist, WishlistItem

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

def products(request, user_id=None):
    if request.method == 'GET':
        error_message = None
        products = list(Product.objects.all())

        # filter
        sports_filter = request.GET.get('sports-filter')
        formal_filter = request.GET.get('formal-filter')
        flipflops_filter = request.GET.get('flipflops-filter')
        casual_filter = request.GET.get('casual-filter')

        filtered_prods = []
        cat_list = []

        if sports_filter:
            sports_prods = Product.objects.filter(category__name="Sports")
            cat_list.append(sports_prods)

        if formal_filter:
            formal_prods = Product.objects.filter(category__name="Formal")
            cat_list.append(formal_prods)

        if flipflops_filter:
            flipflops_prods = Product.objects.filter(category__name="Flip flops")
            cat_list.append(flipflops_prods)

        if casual_filter:
            casual_prods = Product.objects.filter(category__name="Casual")
            cat_list.append(casual_prods)

        for category_products in cat_list:
            for product in category_products:
                filtered_prods.append(product)

        # if filtered list is not empty, set products to filtered product list
        # if filtered list is empty, cat_list is empty i.e. no filter applied
        if filtered_prods:
            products = filtered_prods
        
        # search
        search_term = request.GET.get('inputbar')
        
        if search_term:
            # remove products that don't match search term
            products_copy = products.copy()
            for product in products_copy:
                if search_term.lower() not in product.name.lower():
                    products.remove(product)

            if not products:
                error_message = 'No matches found for "' + search_term + '"' 
        
        # sort
        sort_criterion = request.GET.get('sort')

        if sort_criterion == "sort_price_HtoL":
            products = sorted(products, key=attrgetter('price'), reverse=True)
            
        if sort_criterion == "sort_price_LtoH":
            products = sorted(products, key=attrgetter('price'))

        if sort_criterion == "sort_rating_HtoL":
            products = sorted(
                products, 
                key=lambda product: product.get_avg_rating() if product.get_avg_rating() else 0, 
                reverse=True
            )

        if sort_criterion == "sort_rating_LtoH":
            products = sorted(
                products, 
                key=lambda product: product.get_avg_rating() if product.get_avg_rating() else 0, 
            )

        if sort_criterion == "sort_name_AtoZ":
            products = sorted(products, key=lambda product: product.name.lower())

        if sort_criterion == "sort_name_ZtoA":
            products = sorted(products, key=lambda product: product.name.lower(), reverse=True)
        
        context = {
            'products': products, 
            'error_message': error_message,
            'search_term': search_term,
            'sort_criterion': sort_criterion,
            'sports_filter': sports_filter,
            'formal_filter': formal_filter,
            'flipflops_filter': flipflops_filter,
            'casual_filter': casual_filter
        }
        if user_id:
            curr_user = EcomUser.objects.get(pk=user_id)
            context['curr_user'] = curr_user

        return render(request, 'store/product.html', context=context)

def product_details(request, product_id, user_id=None):
    if request.method == 'GET':
        product = Product.objects.get(id = product_id)
        context = {'product': product}

        if user_id:
            curr_user = EcomUser.objects.get(pk=user_id)
            context['curr_user'] = curr_user

        return render(request, 'store/product-details.html', context=context)

def review(request, user_id, product_id):
    if request.method == 'POST':
        review_text = request.POST['review-text']
        rating = int(request.POST['rating'])

        review_list = list(Review.objects.filter(
            user__pk=user_id,
            product__pk=product_id
        ))

        # if review already exists
        if review_list:
            review = review_list[0]
            review.review_text = review_text
            review.rating = rating

        # if review does not exist, create new review
        else:
            review = Review(
                product=Product.objects.get(pk=product_id),
                user=EcomUser.objects.get(pk=user_id),
                review_text=review_text,
                rating=rating
            )

        review.save()
        return HttpResponseRedirect(reverse('store:product-details', args=(user_id, product_id)))

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
        elif update_method == "remove-all":
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
                        wishlist=curr_user.wishlist, 
                        product=Product.objects.get(pk=cartitem.product.id)
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
        cart.save()
        return HttpResponseRedirect(reverse('store:pay-suc', args=(user_id,)))

def pay_suc(request, user_id):
    curr_user = EcomUser.objects.get(pk=user_id)
    return render(request, 'store/paysuc.html', context={'curr_user': curr_user})

def cancel_order(request, user_id, order_id):
    if request.method == 'POST':
        order = Order.objects.get(pk=order_id)
        order.status = 'X'
        order.save()
        
        return HttpResponseRedirect(reverse('store:account', args=(user_id,)))