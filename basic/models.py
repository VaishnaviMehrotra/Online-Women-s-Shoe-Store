from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address.")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    class Meta:
        db_table = 'User'

    email = models.EmailField(max_length=254, primary_key=True, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name=' last login', auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True)
    phone_number = PhoneNumberField(null=True, blank=False, unique=True)
    university = models.CharField(max_length=300)
    user_type = models.CharField(max_length=40)
    #added_on =models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    #class Meta:
        verbose_name_plural = "User"



class Stock(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    img1 = models.ImageField(upload_to='pics')
    img2 = models.ImageField(upload_to='pics')
    img3 = models.ImageField(upload_to='pics')
    img4 = models.ImageField(upload_to='pics')
    img5 = models.ImageField(upload_to='pics')
    store = models.TextField(max_length=300)
    price = models.IntegerField()
    offer = models.BooleanField(default=False)
    #added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    #class Meta:
        verbose_name_plural = "Stock"




class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True, null=True)
    update_on = models.DateTimeField(auto_now_add=True, null=True)
    #date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.email