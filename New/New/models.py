from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email,username, password, **extra_fields):
        email = self.normalize_email(email)

        user = self.model(email=email,username=username, **extra_fields)

        user.set_password(password)

        user.save()

        return user
    
    def create_superuser(self, email,username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")

        return self.create_user(email=email,username=username, password=password, **extra_fields)
    
class User(AbstractUser):
    email = models.CharField(max_length=80, unique=True)
    username = models.CharField(max_length=45,unique=True)
    # date_of_birth = models.DateField(null=True)
    # uid = models.AutoField(unique=True)
    address = models.TextField(null=True)
    name = models.CharField(max_length=20,null=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
    
class Product(models.Model):
    Pid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    count = models.IntegerField()
    status = models.BooleanField()
    Pimage=models.ImageField(upload_to='Product_images')
    def __str__(self):
        return str(self.Pid)
    
    
class Cart(models.Model):
    Cid = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    Pid = models.ForeignKey(Product,on_delete=models.CASCADE)
    count = models.IntegerField()
    
    def __str__(self):
        val = str(self.Cid)+":"+str(self.Pid)
        return val
    

class Order(models.Model):
    Oid = models.AutoField(primary_key=True)
    Cid = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    products = models.TextField()
    total_price = models.IntegerField()
    date = models.DateTimeField()
    address = models.TextField()
    
    def __str__(self):
        return str(self.Oid)
    
    def add_product(self,pid,count):
        obj = Product.objects.filter(Pid=pid).first()
        obj.count-=count
        if(obj.count==0):
            obj.status=False
        if(self.products==""):
            self.total_price =0
            self.products= str(pid)+":"+str(count) 
            self.total_price = obj.price*count
        else:
            self.products+=","+str(pid)+":"+str(count)
            self.total_price+=obj.price*count
        
        obj.save()
            
    