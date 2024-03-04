from django.contrib import admin
from .models import shoes,gymandaccessories,Winter,Tshirt,MotorSport
# Register your models here.
class shoesadmin(admin.ModelAdmin):
  list_display=('image','sname','sprice','scolor','description')
  fields=['image','sname','sprice','scolor','description']
admin.site.register(shoes,shoesadmin)

class gymandaccessoriesadmin(admin.ModelAdmin):
  list_display=('simage','name','price','color','description')
  fields=['simage','name','price','color','description']
admin.site.register(gymandaccessories,gymandaccessoriesadmin)

class Winteradmin(admin.ModelAdmin):
  list_display=('image','name','price','color','description')
  fields=['image','name','price','color','description']
admin.site.register(Winter,Winteradmin)

class Tshirtadmin(admin.ModelAdmin):
  list_display=('image','name','price','color','description')
  fields=['image','name','price','color','description']
admin.site.register(Tshirt,Tshirtadmin)

class MotorSportadmin(admin.ModelAdmin):
  list_display=('image','name','price','color','description')
  fields=['image','name','price','color','description']
admin.site.register(MotorSport,MotorSportadmin)