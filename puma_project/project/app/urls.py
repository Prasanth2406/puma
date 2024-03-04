from django.urls import path
from . import views
urlpatterns=[
  path("shoe",views.shoe,name="shoe"),
  path("<int:id>",views.shoe_details,name="shoe_details"),
  path("signup",views.signup,name='signup'),
  path("",views.login_view,name=""),
  path("search_result",views.search_result,name='search_result'),
  path("home",views.home,name='home'),
  path("stepin",views.stepin,name='stepin'),
  path("cricket",views.cricket,name="cricket"),
  path("customer",views.customer,name='customer'),
  path("about",views.about,name='about'),
  path("ney",views.ney,name='ney'),
  path("neyvideo",views.neyvideo,name='neyvideo'),
  path('add_to_cart/<int:shoe_id>',views.add_to_cart,name='add_to_cart'),
  path('cart_items',views.cart_items,name='cart_items'),
  path('remove_from_cart/<int:shoe_id>',views.remove_from_cart,name='remove_from_cart'),
  path('add_address',views.add_address,name='add_address'),
  path('set_delivery_address',views.set_delivery_address,name='set_delivery_address'),
  path('order_review/<int:sa_id>',views.order_review,name='order_review'),
  path('checkout_order/<int:sa_id>',views.checkout_order,name='checkout_order'),
  path('payment_order/',views.payment_order,name='payment_order'),
  path('payment-process/<int:order_id>/<int:amount>', views.payment_process, name="payment_process"),
  path('Gymandaccessories',views.Gymandaccessories,name='Gymandaccessories'),
  path(' <int:gid>',views.Gymandacc_details,name='Gymandacc_detail'),
  path('add_to_cart_gym/<int:gym_id>',views.add_to_cart_gym,name='add_to_cart_gym'),
  path('cart_items_gym',views.cart_items_gym,name='cart_items_gym'),
  path('remove_from_cart_gym/<int:gym_id>',views.remove_from_cart_gym,name='remove_from_cart_gym'),
  path('checkout_order_gym/<int:sa_id>',views.checkout_order_gym,name='checkout_order_gym'),
  path('add_address_gym',views.add_address_gym,name='add_address_gym'),
  path('order_review_gym/<int:sa_id>',views.order_review_gym,name='order_review_gym'),
  path('winter',views.winter,name='winter'),
  path('  <int:wid>',views.winter_details,name='winter_details'),
  path('add_to_cart_winter/<int:wid>',views.add_to_cart_winter,name='add_to_cart_winter'),
  path('cart_items_winter',views.cart_items_winter,name='cart_items_winter'),
  path('remove_from_cart_winter/<int:wid>',views.remove_from_cart_winter,name='remove_from_cart_winter'),
  path('checkout_order_winter/<int:sa_id>',views.checkout_order_winter,name='checkout_order_winter'),
  path('add_address_winter',views.add_address_winter,name='add_address_winter'),
  path('order_review_winter/<int:sa_id>',views.order_review_winter,name='order_review_winter'),
  path('shirt',views.shirt,name='shirt'),
  path('   <int:wid>',views.shirt_details,name='shirt_details'),
  path('add_to_cart_shirt/<int:wid>',views.add_to_cart_shirt,name='add_to_cart_shirt'),
  path('cart_items_shirt',views.cart_items_shirt,name='cart_items_shirt'),
  path('remove_from_cart_shirt/<int:wid>',views.remove_from_cart_shirt,name='remove_from_cart_shirt'),
  path('checkout_order_shirt/<int:sa_id>',views.checkout_order_shirt,name='checkout_order_shirt'),
  path('add_address_shirt',views.add_address_shirt,name='add_address_shirt'),
  path('order_review_shirt/<int:sa_id>',views.order_review_shirt,name='order_review_shirt'),
  path('motor',views.motor,name='motor'),
  path('    <int:wid>',views.motor_details,name='motor_details'),
  path('add_to_cart_motor/<int:wid>',views.add_to_cart_motor,name='add_to_cart_motor'),
  path('cart_items_motor',views.cart_items_motor,name='cart_items_motor'),
  path('remove_from_cart_motor/<int:wid>',views.remove_from_cart_motor,name='remove_from_cart_motor'),
  path('checkout_order_motor/<int:sa_id>',views.checkout_order_motor,name='checkout_order_motor'),
  path('add_address_motor',views.add_address_motor,name='add_address_motor'),
  path('order_review_motor/<int:sa_id>',views.order_review_motor,name='order_review_motor'),
]