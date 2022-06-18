from django import forms
from django.db.models import fields
from django.forms import ModelForm
from .models import *

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user','email']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['firstname','lastname','phone','profile_photo']
        
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','phone','email','county','town','order_note']

class PaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].required = True
        
    class Meta:
        model = Pay
        fields = ['first_name', 'last_name', 'phone']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']