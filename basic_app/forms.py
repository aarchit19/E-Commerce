from django import forms
from basic_app.models import CustProfileInfo,VendorProfileInfo,SoldItem
from django.contrib.auth.models import User

class customer_profile:
    class UserForm(forms.ModelForm):
        password=forms.CharField(widget=forms.PasswordInput())
        confirm_password=forms.CharField(widget=forms.PasswordInput())
        class Meta():
            model = User
            fields=('username','email','password','confirm_password')

    class UserProfileInfoForm(forms.ModelForm):
        class Meta():
            model = CustProfileInfo
            fields=('Name','Phone','Address','Zipcode')

class vendor_profile:
    class UserForm(forms.ModelForm):
        password=forms.CharField(widget=forms.PasswordInput())
        confirm_password=forms.CharField(widget=forms.PasswordInput())
        class Meta():
            model = User
            fields=('username','email','password','confirm_password')
    class UserProfileInfoForm(forms.ModelForm):
        class Meta():
            model = VendorProfileInfo
            fields=('Name','Phone','Address','Shop_Name')

class item_form(forms.ModelForm):
    class Meta():
        model = SoldItem
        fields = ('name','picture','description','price','available_quantity')
