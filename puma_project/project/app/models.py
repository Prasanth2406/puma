from django.db import models
from django.contrib.auth.models import User

class gymandaccessories(models.Model):
  simage = models.ImageField(upload_to='gym_images')
  name=models.CharField(max_length=50)
  price=models.IntegerField()
  color=models.CharField(max_length=50)
  description=models.CharField(max_length=500)

class shoes(models.Model):
  image=models.ImageField(upload_to="shoe_images")
  sname=models.CharField(max_length=50)
  sprice=models.IntegerField()
  scolor=models.CharField(max_length=50)
  description=models.CharField(max_length=500)

class Winter(models.Model):
  image = models.ImageField(upload_to='winter_images')
  name=models.CharField(max_length=50)
  price=models.IntegerField()
  color=models.CharField(max_length=50)
  description=models.CharField(max_length=500)

class Tshirt(models.Model):
  image = models.ImageField(upload_to='tshirt_images')
  name=models.CharField(max_length=50)
  price=models.IntegerField()
  color=models.CharField(max_length=50)
  description=models.CharField(max_length=500)

class MotorSport(models.Model):
  image = models.ImageField(upload_to='motor_images')
  name=models.CharField(max_length=50)
  price=models.IntegerField()
  color=models.CharField(max_length=50)
  description=models.CharField(max_length=500)

class Customer(models.Model):
  user=models.OneToOneField(User,on_delete=models.CASCADE)
  phone=models.CharField(max_length=10,default='NA')
  def str(self):
    return self.user.username
  
class Cartitem(models.Model):
  customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
  quantity=models.IntegerField(default=0)
  size=models.CharField(max_length=2,null=True, blank=True)
  shoe=models.ForeignKey(shoes,on_delete=models.CASCADE,null=True)
  gym=models.ForeignKey(gymandaccessories,on_delete=models.CASCADE,null=True)
  winter=models.ForeignKey(Winter,on_delete=models.CASCADE,null=True)
  shirt=models.ForeignKey(Tshirt,on_delete=models.CASCADE,null=True)
  ms=models.ForeignKey(MotorSport,on_delete=models.CASCADE,null=True)
  class Meta:
    db_table='cart_items'

  def _str_(self):
    return self.shoe.sname
  def _str_(self):
    return self.gym.name
  def _str_(self):
    return self.winter.name
  def _str_(self):
    return self.shirt.name
  def _str_(self):
    return self.ms.name
  
class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    building_name=models.CharField(max_length=200,null=False)
    street=models.CharField(max_length=200,null=False)
    landmark=models.CharField(max_length=200,blank=True,null=True)
    city=models.CharField(max_length=200,blank=True,null=True)
    state=models.CharField(max_length=30,null=False)
    zipcode=models.CharField(max_length=6,null=False)
    date_added=models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False)
    transaction_id=models.CharField(max_length=100,null=True)
    shipping_address=models.ForeignKey(ShippingAddress,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return str(self.id)
    def get_total_cost(self):
        return sum(item.get_cost() for item  in self.items.all())

class OrderItem(models.Model):
    product=models.ForeignKey(shoes,on_delete=models.SET_NULL,null=True)
    products=models.ForeignKey(gymandaccessories,on_delete=models.SET_NULL,null=True)
    productss=models.ForeignKey(Winter,on_delete=models.SET_NULL,null=True)
    prod=models.ForeignKey(Tshirt,on_delete=models.SET_NULL,null=True)
    prods=models.ForeignKey(MotorSport,on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,related_name='items',on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField(default=9,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)

    def get_cost(self):
        return self.price * self.quantity