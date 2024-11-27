from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import models
from django import forms
from .models import *
from django import forms
import uuid


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username","first_name","email", "last_name","password1","password2")
        widgets={
        'password':  forms.PasswordInput(attrs={'class': 'password'}),
        
   		 }

class Contact(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = '__all__'
class AddressForm(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = ('name',
					'email',
					'address', 
					'country',
					'state',
					'zipcode')
        widgets = {
        	'name': forms.TextInput(attrs={'placeholder':'Name'}),
        	'email': forms.TextInput(attrs={'placeholder':'Email'}),
        	'address': forms.TextInput(attrs={'placeholder':'Address'}),
        	'country': forms.TextInput(attrs={'placeholder':'Country'}),
        	'state': forms.TextInput(attrs={'placeholder':'State'}),
        	'zipcode': forms.TextInput(attrs={'placeholder':'ZipCode'}),
        }
    


class DriverSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password1', 'password2', 'first_name', 'last_name']  # Removed 'username' from fields since it's auto-generated

    def save(self, commit=True):
        # Override the save method to create a DeliveryDriver profile
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        # Auto-generate a username using UUID
        user.username = str(uuid.uuid4().int)[:9]  # Generate a 9-digit number

        if commit:
            user.save()
            # Create a DeliveryDriver profile linked to this user
            phone_number = self.cleaned_data['phone_number']
            DeliveryDriver.objects.create(user=user, phone_number=phone_number)
        return user


class DeliveryStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['status']  # We are only updating the status field

    status = forms.ChoiceField(choices=Delivery.ORDER_STATUS_CHOICES, label="Delivery Status", widget=forms.Select())