from django.shortcuts import render,redirect
from basic_app.models import CustProfileInfo,VendorProfileInfo,SoldItem,PurchasedItem,CartItem,WishList
from django.contrib.auth.models import User
from basic_app.forms import customer_profile,vendor_profile,item_form
from django.contrib import messages
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import xlwt
from xlwt import Workbook
from django.core.files.storage import FileSystemStorage
import xlrd

host_user=settings.DEFAULT_FROM_EMAIL

def index(request):
    return render(request,'basic_app/home.html')



class customer():
    def register(request):
        registered=False

        if request.method=='POST':
            cust_user_form=customer_profile.UserForm(request.POST)
            cust_profile_form = customer_profile.UserProfileInfoForm(request.POST)
            username=request.POST.get('username')
            email=request.POST.get('email')
            password1=request.POST['password']
            password2=request.POST['confirm_password']
            if password1==password2:
                if cust_user_form.is_valid() and cust_profile_form.is_valid():
                    user = cust_user_form.save(commit=False)
                    user.save()
                    user.set_password(user.password)
                    user.first_name="customer"
                    user.save()
                    profile=cust_profile_form.save(commit=False)
                    profile.user = user
                    profile.save()

                    registered=True
                    user=authenticate(username=username,password=password1)
                    login(request,user)
                    return redirect('/basic_app/customer_home')
                else:
                    return HttpResponse(cust_user_form.errors,cust_profile_form.errors)
            else:
                return HttpResponse("'<script>alert(\'Passwords do not match\');</script>'")
        else:
            cust_user_form=customer_profile.UserForm()
            cust_profile_form = customer_profile.UserProfileInfoForm()
        return render(request,'basic_app/custregister.html',{'cust_user_form':cust_user_form,'cust_profile_form':cust_profile_form,
        'registered':registered})

    def user_login(request):
        if request.method=='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username,password=password)
            try:
                profile=User.objects.get(username=username,first_name="customer")
            except:
                return HttpResponse("'<script>alert(\'You are not a Customer\');</script>'")
            if user:
                if user.is_active:
                    login(request,user)
                    return redirect('/basic_app/customer_home')
                else:
                    return HttpResponse("'<script>alert(\'Account not active\');</script>'")
            else:
                return HttpResponse('<script>alert(\'Invalid login details\');</script>')
        else:
            return render(request,'basic_app/home.html',{})


class vendor():


    def register(request):
        registered=False

        if request.method=='POST':
            vendor_user_form=vendor_profile.UserForm(request.POST)
            vendor_profile_form = vendor_profile.UserProfileInfoForm(request.POST)

            username=request.POST.get('username')
            email=request.POST.get('email')
            password1=request.POST.get('password')
            password2=request.POST.get('confirm_password')
            if password1==password2:
                if vendor_user_form.is_valid() and vendor_profile_form.is_valid():
                    user = vendor_user_form.save()
                    user.save()
                    user.set_password(user.password)
                    user.first_name="vendor"
                    user.save()
                    profile=vendor_profile_form.save(commit=False)
                    profile.user = user
                    profile.save()
                    registered=True
                    user=authenticate(username=username,password=password1)
                    login(request,user)
                    return redirect('/basic_app/vendor_home')
                else:
                    return HttpResponse(vendor_user_form.errors,vendor_profile_form.errors)
            else:
                return HttpResponse('<script>alert(\'Passwords do not match\');</script>')
        else:
            vendor_user_form=vendor_profile.UserForm()
            vendor_profile_form = vendor_profile.UserProfileInfoForm()
        return render(request,'basic_app/vendorregister.html',{'vendor_user_form':vendor_user_form,'vendor_profile_form':vendor_profile_form,
        'registered':registered})

    def user_login(request):
        if request.method=='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username,password=password)
            try:
                profile=User.objects.get(username=username,first_name="vendor")
            except:
                return HttpResponse("'<script>alert(\'You are not a Vendor\');</script>'")
            if user:
                if user.is_active:
                    login(request,user)
                    return redirect('/basic_app/vendor_home')
                else:
                    return HttpResponse("'<script>alert(\'Account not active\');</script>'")
            else:
                return HttpResponse('<script>alert(\'Invalid login details\');</script>')
        else:
            return render(request,'basic_app/home.html',{})

@login_required
def user_logout(request):
    return HttpResponseRedirect(reverse('index'))

def VendorHome(request):
    current_user=request.user
    user=User.objects.get(first_name='vendor',username=current_user.username)
    vendor=VendorProfileInfo.objects.get(user_id=user.id)
    items=SoldItem.objects.filter(vendor=vendor).order_by('id')

    if vendor is None:
        return render(request, 'basic_app/home.html',{"message":"Login again"})

    return render(request, 'basic_app/vendor_home.html', {'user':user,'vendor':vendor, 'items':items})

def CustomerHome(request):
    current_user=request.user
    user=User.objects.get(first_name='customer',username=current_user.username)
    customer=CustProfileInfo.objects.get(user_id=user.id)
    items=SoldItem.objects.all().order_by('-sold_quantity')

    if customer is None:
        return render(request, 'basic_app/home.html',{"message":"Login again"})

    return render(request, 'basic_app/cust_home.html', {'user':user,'customer':customer, 'items':items,})

def Additems(request):
    current_user=request.user
    user=User.objects.get(first_name='vendor',username=current_user.username)
    vendor=VendorProfileInfo.objects.get(user_id=user.id)
    if request.method == 'POST':
        items=item_form(request.POST,request.FILES)
        if items.is_valid():
            form=items.save(commit=False)
            form.vendor=vendor
            form.save()
            return redirect('/basic_app/add_item')
        else:
            return HttpResponse(items.errors)
    else:
        form=item_form()
    return render(request,'basic_app/additem.html',{'user':user,'vendor':vendor,'form':form})

def deleteitems(request):
    current_user=request.user
    user=User.objects.get(first_name='vendor',username=current_user.username)
    vendor=VendorProfileInfo.objects.get(user_id=user.id)
    itemid=request.POST['item_id']
    item=SoldItem.objects.get(id=itemid)
    if vendor.id==item.vendor_id:
        item.delete()
    return redirect('/basic_app/vendor_home')

def edititems(request):
    current_user=request.user
    user=User.objects.get(first_name='vendor',username=current_user.username)
    vendor=VendorProfileInfo.objects.get(user_id=user.id)
    itemid=request.POST['item_id']
    item=SoldItem.objects.get(id=itemid)
    return render(request,'basic_app/edititem.html',{'user':user,'vendor':vendor,'item':item})

def edititems_submit(request):
    current_user=request.user
    user=User.objects.get(first_name='vendor',username=current_user.username)
    vendor=VendorProfileInfo.objects.get(user_id=user.id)
    itemid=request.POST['item_id']
    prev_item=SoldItem.objects.get(id=itemid)
    if request.FILES.get('picture'):
        item=SoldItem(id=itemid, name=request.POST['name'], picture=request.FILES['picture'], price=request.POST['price'], description=request.POST['description'], available_quantity=request.POST['available_quantity'],vendor_id=vendor.id)
        item.save()
    else:
        item=SoldItem(id=itemid, name=request.POST['name'], picture= prev_item.picture, price=request.POST['price'], description=request.POST['description'], available_quantity=request.POST['available_quantity'],vendor_id=vendor.id)
        item.save()
    return redirect('/basic_app/vendor_home')


def ChangeAddress(request):
    current_user=request.user
    user=User.objects.get(first_name='customer',username=current_user.username)
    customer=CustProfileInfo.objects.get(user_id=user.id)
    if request.method=='POST':
        address=request.POST['address']
        customer.Address=address
        customer.save()
        return redirect('/basic_app/customer_home')
    else:
        return render(request,'basic_app/changeaddress.html',{'user':user,'customer':customer})

def AddBalance(request):
    current_user=request.user
    user=User.objects.get(first_name='customer',username=current_user.username)
    customer=CustProfileInfo.objects.get(user_id=user.id)
    if request.method=='POST':
        balance=request.POST['wallet_balance']
        customer.wallet_balance+=int(balance)
        customer.save()
        return redirect('/basic_app/customer_home')
    else:
        return render(request,'basic_app/walletmoney.html',{'user':user,'customer':customer})

def AddItemToCart(request):
    current_user=request.user
    user=User.objects.get(first_name='customer',username=current_user.username)
    customer=CustProfileInfo.objects.get(user_id=user.id)
    item_id=request.POST['Cartbtn']
    item=SoldItem.objects.get(id=item_id)
    requested_quantity=request.POST['quantity']

    if int(requested_quantity) > item.available_quantity:
        messages.info(request, 'Item is not available in requested quantity')
        return redirect('/basic_app/customer_home')

    cartitems=CartItem.objects.filter(customer_id=customer.id)

    for cartitem in cartitems:
        if cartitem.item == item:
            current_user=request.user
            user=User.objects.get(first_name='customer',username=current_user.username)
            customer=CustProfileInfo.objects.get(user_id=user.id)
            items=SoldItem.objects.all().order_by('-sold_quantity')
            items.reverse()
            return render(request, 'basic_app/cust_home.html', {'user':user,'customer':customer, 'items':items, 'message':'Item is already in Cart'})
    cost=int(item.price) * int(requested_quantity)
    cart=CartItem(customer_id=customer.id, item_id=item.id, requested_quantity=requested_quantity, cost=cost)
    cart.save()

    return redirect('/basic_app/customer_home')

def AddItemToWishList(request):
    current_user=request.user
    user=User.objects.get(first_name='customer',username=current_user.username)
    customer=CustProfileInfo.objects.get(user_id=user.id)
    item_id=request.POST['wishlistbtn']
    item=SoldItem.objects.get(id=item_id)
    wishlistitems=WishList.objects.filter(customer_id=customer.id)

    for listitem in wishlistitems:
        if listitem.item == item:
            current_user=request.user
            user=User.objects.get(first_name='customer',username=current_user.username)
            customer=CustProfileInfo.objects.get(user_id=user.id)
            items=SoldItem.objects.all().order_by('-sold_quantity')
            items.reverse()
            return render(request, 'basic_app/cust_home.html', {'user':user,'customer':customer, 'items':items, 'message':'Item is already in WishList'})
    wishlist=WishList(customer_id=customer.id, item_id=item.id)
    wishlist.save()

    return redirect('/basic_app/customer_home')

def cart(request):
    current_user=request.user
    user=User.objects.get(first_name='customer',username=current_user.username)
    customer=CustProfileInfo.objects.get(user_id=user.id)
    items=CartItem.objects.filter(customer_id=customer.id)
    return render(request,'basic_app/cart.html',{'user':user,'customer':customer,'items':items})

def wishlist(request):
    current_user=request.user
    user=User.objects.get(first_name='customer',username=current_user.username)
    customer=CustProfileInfo.objects.get(user_id=user.id)
    items=WishList.objects.filter(customer_id=customer.id)
    return render(request,'basic_app/wishlist.html',{'user':user,'customer':customer,'items':items})


def DeleteItemFromCart(request):
    item=request.POST['removebtn']
    item=CartItem.objects.get(id=item)
    item.delete()
    return redirect('/basic_app/Cart')

def DeleteItemFromWishList(request):
    item=request.POST['removebtn']
    item=WishList.objects.get(id=item)
    item.delete()
    return redirect('/basic_app/WishList')

def BuyItem(request):
    #recieved value is a CartItem id
    current_user=request.user
    id=request.POST['Buybtn']
    BoughtItem=CartItem.objects.get(id=id)
    user=User.objects.get(first_name='customer',username=current_user.username)
    customer=CustProfileInfo.objects.get(user_id=user.id)
    items=CartItem.objects.filter(customer_id=customer.id)

    if BoughtItem.requested_quantity > BoughtItem.item.available_quantity:
        return render(request, 'basic_app/cart.html', {'items':items, 'customer':customer, 'message':'Requested quantity not available'})

    if BoughtItem.customer.wallet_balance < BoughtItem.cost:
        return render(request, 'basic_app/cart.html', {'items':items, 'customer':customer, 'message':'Your wallet do not have enough balance'})

    customer.wallet_balance = customer.wallet_balance - BoughtItem.cost
    #customer.has_ordered_item=True
    customer.save()

    item=SoldItem.objects.get(id=BoughtItem.item_id)
    item.available_quantity = item.available_quantity - BoughtItem.requested_quantity
    item.sold_quantity = item.sold_quantity + BoughtItem.requested_quantity
    item.save()

    purchase=PurchasedItem(customer=customer, item=item, quantity=BoughtItem.requested_quantity, cost=BoughtItem.cost)
    purchase.save()

    subject = 'New Purchase of ' + item.name
    message = user.username + ' purchased ' + str(BoughtItem.requested_quantity)+ ' ' +item.name
    recepient=BoughtItem.item.vendor.user.email

    send_mail(subject, message, host_user, [recepient], fail_silently = False)

    BoughtItem.delete()

    return redirect('/basic_app/CustomerOrderHistory')

def CustomerOrderHistory(request):
    current_user=request.user
    user=User.objects.get(first_name='customer',username=current_user.username)
    customer=CustProfileInfo.objects.get(user_id=user.id)
    purchases=PurchasedItem.objects.filter(customer_id=customer.id)

    return render(request, 'basic_app/CustOrderHistory.html', {'items':purchases, 'customer':customer})

def CompleteOrder(request):
    current_user=request.user
    user=User.objects.get(first_name='customer',username=current_user.username)
    customer=CustProfileInfo.objects.get(user_id=user.id)
    id=request.POST['CompOrdbtn']
    item=PurchasedItem.objects.get(id=id)
    item.order_complete=True
    item.save()
    return redirect('/basic_app/CustomerOrderHistory')

def ViewOrders(request):
    current_user=request.user
    user=User.objects.get(first_name='vendor',username=current_user.username)
    vendor=VendorProfileInfo.objects.get(user_id=user.id)
    items=SoldItem.objects.filter(vendor_id=vendor.id)
    purchases=PurchasedItem.objects.none()
    for item in items:
        purchases=purchases|PurchasedItem.objects.filter(item_id=item.id)

    return render(request, 'basic_app/ViewOrders.html', {'user':user,'vendor':vendor, 'items':purchases})

def FindUser(request):
    current_user=request.user

    try:
        user=User.objects.get(email=current_user.email)
        vendor=VendorProfileInfo.objects.get(user_id=user.id)
    except :
        vendor=None

    if vendor is not None :
        return redirect('/basic_app/VendorHome')

    try :
        user=User.objects.get(email=current_user.email)
        customer=CustProfileInfo.objects.get(user_id=user.id)
    except :
        customer=None

    if customer is not None:
        return redirect('/basic_app/CustomerHome')

    return redirect('/basic_app/GoogleHome')


def GoogleHome(request):
    current_user=request.user
    return render(request, 'basic_app/GoogleHome.html', {'current_user':current_user})

def googlecustomer(request):
    current_user=request.user
    user=User(first_name='customer',username=current_user.username, email=current_user.email)
    user.save()
    customer=Customer(user_id=user.id)
    customer.save()
    return redirect('basic_app/customer_home')

def googlevendor(request):
    current_user=request.user
    user=User(first_name='vendor',username=current_user.username, email=current_user.email)
    user.save()
    vendor=Vendor(user_id=user.id)
    vendor.save()
    return redirect('basic_app/vendor_home')

def GenerateReport(request):
    current_user=request.user
    user=User.objects.get(username=current_user.username)
    vendor=VendorProfileInfo.objects.get(user_id=user.id)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="orders.xls"'

    wb=xlwt.Workbook()
    sheet1=wb.add_sheet('Sheet 1')

    sheet1.write(0,0,'Customer')
    sheet1.write(0,1,'Item')
    sheet1.write(0,2,'Price')
    sheet1.write(0,3,'Quantity')
    sheet1.write(0,4,'Amount')
    sheet1.write(0,5,'Order Completed')
    i=1
    items=SoldItem.objects.filter(vendor_id=vendor.id)

    purchases=PurchasedItem.objects.none()

    for item in items:
        purchases=purchases|PurchasedItem.objects.filter(item=item)

    for purchase in purchases:
        sheet1.write(i,0,purchase.customer.user.username)
        sheet1.write(i,1,purchase.item.name)
        sheet1.write(i,2,purchase.item.price)
        sheet1.write(i,3,purchase.quantity)
        sheet1.write(i,4,purchase.cost)
        sheet1.write(i,5,purchase.order_complete)
        i=i+1
    file_name=user.username+'.xls'

    wb.save(response)

    vendor.order_history=file_name
    vendor.save()

    return (response)
