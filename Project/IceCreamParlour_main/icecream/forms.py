from django import forms
from .models import Icecream
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# class IceForm(forms.Form):
#     topping1 = forms.CharField(label='Topping 1', max_length=100)
#     topping2 = forms.CharField(label='Topping 2', max_length=100)
#     size = forms.ChoiceField(label='size', choices=[('cup', 'cup'), ('Regular', 'Regular'), ('Large', 'Large')])

class IceForm(forms.ModelForm):
    class Meta:
        model = Icecream
        fields = ['topping1', 'topping2', 'size']
        labels = {'topping1': 'Topping 1', 'topping2': 'Topping 2'}


class MultipleIceForm(forms.Form):
    numofice = forms.IntegerField(min_value=2, max_value=10)


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
