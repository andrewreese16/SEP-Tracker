from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.db.models import Q
from datetime import date
from .models import Customer
from .forms import CustomerForm, CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form}) 


@login_required
def dashboard(request):
    # Fetching customers created by the logged-in user
    customers = Customer.objects.filter(created_by=request.user)
    upcoming_sep_ends = customers.filter(
        sep_end_date__gte=date.today()
    ).order_by('sep_end_date')
    
    return render(request, 'enrollments/dashboard.html', {
        'customers': upcoming_sep_ends,
    })

@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user  # Assign the logged-in user
            customer.save()
            messages.success(request, 'Customer added successfully.')
            return redirect('dashboard')  # Redirect to the dashboard after saving
    else:
        form = CustomerForm()  # Create a new form instance
    
    return render(request, 'enrollments/customer_form.html', {'form': form})

@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)  # Bind the form with the existing customer
        if form.is_valid():
            form.save()  # Save the updated customer
            messages.success(request, 'Customer updated successfully.')
            return redirect('dashboard')  # Redirect to the dashboard after saving
    else:
        form = CustomerForm(instance=customer)  # Create a form with the existing customer data
    
    return render(request, 'enrollments/customer_form.html', {'form': form})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk, created_by=request.user)
    if request.method == 'POST':
        customer.delete()  # Delete the customer instance
        messages.success(request, 'Customer deleted successfully.')
        return redirect('dashboard')  # Redirect to the dashboard after deletion
    
    return render(request, 'enrollments/customer_confirm_delete.html', 
                  {'customer': customer})  # Show confirmation page

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in after registration
            messages.success(request, 'Registration successful! You are now logged in.')
            return redirect('dashboard')  # Redirect to the dashboard after registration
    else:
        form = CustomUserCreationForm()  # Create a new form instance
    
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def search_customers(request):
    query = request.GET.get('q', '')
    customers = Customer.objects.filter(
        created_by=request.user
    ).filter(
        Q(full_name__icontains=query) | Q(email__icontains=query)
    )
    return render(request, 'enrollments/search_results.html', {'customers': customers})
