from django.shortcuts import render, redirect
from .forms import IceForm, MultipleIceForm
from django.forms import formset_factory
from .models import Icecream
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm


def home(request):
    return render(request, 'icecream/home.html')


def order(request):
    multiple_form = MultipleIceForm()
    if request.method == 'POST':
        filled_form = IceForm(request.POST)
        if filled_form.is_valid():
            prepared_icecream = filled_form.save()
            prepared_icecream_pk = prepared_icecream.id
            note = 'Thanks for ordering! Your %s %s and %s IceCream is on the way!' % (filled_form.cleaned_data['size'],
                                                                                       filled_form.cleaned_data[
                                                                                           'topping1'],
                                                                                       filled_form.cleaned_data[
                                                                                           'topping2'])
            new_form = IceForm()
            return render(request, 'icecream/order.html',
                          {'prepared_icecream_pk': prepared_icecream_pk, 'IceForm': new_form, 'note': note,
                           'multiple_form': multiple_form})
    else:
        form = IceForm()
        return render(request, 'icecream/order.html', {'IceForm': form, 'multiple_form': multiple_form})


def icecream(request):
    num_of_icecream = 2
    filled_multi_ice_form = MultipleIceForm(request.GET)
    if filled_multi_ice_form.is_valid():
        num_of_icecream = filled_multi_ice_form.cleaned_data['numofice']
    IceFormSet = formset_factory(IceForm, extra=num_of_icecream)
    formset = IceFormSet()
    if request.method == 'POST':
        filled_formset = IceFormSet(request.POST)
        if filled_formset.is_valid():
            for form in filled_formset:
                print(form.cleaned_data['topping1'])
                note = 'IceCream has been ordered'
        else:
            note = 'Order has not been created, please try again!'

        return render(request, 'icecream/icecream.html', {'note': note, 'formset': formset})
    else:
        return render(request, 'icecream/icecream.html', {'formset': formset})


def edit_order(request, pk):
    icecream = Icecream.objects.get(pk=pk)
    form = IceForm(instance=icecream)
    if request.method == 'POST':
        filled_form = IceForm(request.POST, instance=icecream)
        if filled_form.is_valid():
            filled_form.save()
            form = filled_form
            note = "Order has been Update"
            return render(request, 'icecream/edit_order.html', {'note': note, 'IceForm': form, 'icecream': icecream})

    return render(request, 'icecream/edit_order.html', {'IceForm': form, 'icecream': icecream})


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("icecream:home")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request=request,
                          template_name="icecream/register.html",
                          context={"form": form})

    form = UserCreationForm
    return render(request=request,
                  template_name="icecream/register.html",
                  context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("icecream:home")


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="icecream/login.html",
                  context={"form": form})
