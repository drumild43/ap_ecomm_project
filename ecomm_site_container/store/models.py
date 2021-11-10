from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

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

class EcomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        user = self.model(email=self.normalize_email(email))
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
    cart = models.OneToOneField('Cart', on_delete=models.SET_NULL, null=True)
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
    CANCELLED = 'X'
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