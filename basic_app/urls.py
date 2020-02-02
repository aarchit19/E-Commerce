from django.urls import path
from basic_app import views

app_name = 'basic_app'

urlpatterns = [
    path('customer/register/',views.customer.register,name="cust_register"),
    path('vendor/register',views.vendor.register,name="vendor_register"),
    path('customer/login',views.customer.user_login,name='cust_login'),
    path('vendor/login',views.vendor.user_login,name='vendor_login'),
    path('vendor_home/',views.VendorHome,name='vendor_home'),
    path('customer_home',views.CustomerHome,name='customer_home'),
    path('add_item',views.Additems,name='add_item'),
    path('DeleteItem',views.deleteitems,name='DeleteItem'),
    path('EditItem',views.edititems,name='EditItem'),
    path('EditItemSubmit',views.edititems_submit,name='EditItemSubmit'),
    path('ChangeAddress',views.ChangeAddress,name='ChangeAddress'),
    path('AddBalance',views.AddBalance,name='AddBalance'),
    path('AddItemToCart',views.AddItemToCart,name='AddItemToCart'),
    path('AddItemToWishList',views.AddItemToWishList,name='AddItemToWishList'),
    path('Cart',views.cart,name='Cart'),
    path('WishList',views.wishlist,name='WishList'),
    path('DeleteItemFromWishList',views.DeleteItemFromWishList,name='DeleteItemFromWishList'),
    path('DeleteItemFromCart',views.DeleteItemFromCart,name='DeleteItemFromCart'),
    path('BuyItem',views.BuyItem,name='BuyItem'),
    path('CustomerOrderHistory',views.CustomerOrderHistory,name='CustomerOrderHistory'),
    path('CompletedOrder',views.CompleteOrder,name='CompletedOrder'),
    path('ViewOrders',views.ViewOrders,name='ViewOrders'),
    path('FindUser',views.FindUser,name='FindUser'),
    path('GoogleHome',views.GoogleHome,name='GoogleHome'),
    path('google_vendor',views.googlevendor,name='google_vendor'),
    path('google_customer',views.googlecustomer,name='google_customer'),
    path('export/xls/', views.GenerateReport, name='export_orders'),
]
