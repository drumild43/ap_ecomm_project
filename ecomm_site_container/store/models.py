import datetime

from django.db import models
from django.db.models import Avg, Count
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def get_img_name(self):
        return "store/images/" + self.name + ".jpg"

    def get_avg_rating(self):
        avg_rating = Review.objects.filter(
                product__pk=self.id
            ).aggregate(
                Avg('rating')
            )['rating__avg']

        return avg_rating
    
    def get_review_count(self):
        review_count = Product.objects.filter(
                pk=self.id
            ).annotate(
                Count('review')
            )[0].review__count

        return review_count

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class EcomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        cart = Cart()
        wishlist = Wishlist()
        user = self.model(email=self.normalize_email(email), cart=cart, wishlist=wishlist)
        cart.save()
        wishlist.save()
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class EcomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True)
    cart = models.OneToOneField('Cart', on_delete=models.SET_NULL, null=True, blank=True)
    wishlist = models.OneToOneField('Wishlist', on_delete=models.DO_NOTHING, blank=True)
    logged_in = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)

    objects = EcomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Cart(models.Model):
    total_quantity = models.PositiveIntegerField(default=0)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    size = models.PositiveSmallIntegerField(null=True)

class Wishlist(models.Model):
    pass

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Order(models.Model):
    user = models.ForeignKey(EcomUser, on_delete=models.CASCADE)
    ordered_on = models.DateTimeField(auto_now_add=True)
    order_total = models.PositiveIntegerField()
    total_quantity = models.PositiveIntegerField()

    CONFIRMED = 'C'
    TRANSIT = 'T'
    DELIVERED = 'D'
    CANCELLED = 'X'
    STATUS_CHOICES = [
        (CONFIRMED, 'Confirmed'),
        (TRANSIT, 'In Transit'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled')
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=CONFIRMED)

    def get_updated_status(self):
        # if order not cancelled or delivered, update status according to order time
        if self.status != 'X' and self.status != 'D':
            time_passed = timezone.now() - self.ordered_on
            
            if time_passed < datetime.timedelta(minutes=30):
                self.status = 'C'

            elif time_passed < datetime.timedelta(minutes=60):
                self.status = 'T'

            else:
                self.status = 'D'

            self.save()

        return self.get_status_display()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    size = models.PositiveSmallIntegerField(null=True)

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(EcomUser, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField()

    def is_by_verified_buyer(self):
        # list of user's orders with given product
        orders = Order.objects.filter(
            user__pk=self.user.id, 
            orderitem__product__pk=self.product.id
        )

        for order in orders:
            # buyer verified if there is a delivered order with given product
            if order.get_updated_status() == 'Delivered':
                return True