from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    price = models.PositiveIntegerField()

    """
    def get_img_name(self):
        return "img" + str(self.id)
    """
    # avg_rating
    # ^^ average of user ratings; probably computed instead of related to ratings model
    # review_count

class Category(models.Model):
    name = models.CharField(max_length=100)

class EcomUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_num = models.CharField(max_length=20)
    cart = models.OneToOneField('Cart', on_delete=models.SET_NULL, null=True)
    # password?

class Cart(models.Model):
    pass

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

class Order(models.Model):
    ordered_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(EcomUser, on_delete=models.CASCADE)

    CONFIRMED = 'C'
    TRANSIT = 'T'
    DELIVERED = 'D'
    CANCELLED = 'C'
    STATUS_CHOICES = [
        (CONFIRMED, 'Confirmed'),
        (TRANSIT, 'In Transit'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=CONFIRMED)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()

"""
class Review(models.Model):
    pass

class Rating(models.Model):
    pass
"""