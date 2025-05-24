from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm,ProductForm, ReviewForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from .models import Product
from django.db.models import Avg

from .forms import SignupForm

User = get_user_model()

def signup_view(request):
    form = SignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        user.assign_group()
        login(request, user)
        if user.is_admin:
            return redirect('admin_dashboard')
        return redirect('user_dashboard')
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        if user.is_admin:
            return redirect('admin_dashboard')
        return redirect('user_dashboard')
    return render(request, 'login.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_user)
def user_dashboard(request):
    products = Product.objects.annotate(avg_rating=Avg('reviews__rating'))
    return render(request, 'user_dashboard.html', {'products': products})


@login_required
@user_passes_test(lambda u: u.is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ProductForm()
    products = Product.objects.all().prefetch_related('reviews')
    return render(request, 'admin_dashboard.html', {'form': form, 'products': products})


def is_user(user):
    return user.is_authenticated and user.role == 'user'

@login_required
@user_passes_test(is_user)
def user_dashboard(request):
    products = Product.objects.annotate(avg_rating=Avg('reviews__rating'))
    return render(request, 'user_dashboard.html', {'products': products})

@login_required
@user_passes_test(is_admin)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('admin_dashboard')
    
@login_required
@user_passes_test(is_admin)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('admin_dashboard')
    return render(request, 'add_product.html', {
        'form': form,
        'product': product,
        'is_edit': True
    })

@login_required
@user_passes_test(is_admin)
def edit_product_list(request):
    products = Product.objects.all()
    return render(request, 'edit_product_list.html', {'products': products})

@login_required
@user_passes_test(is_admin)
def delete_product_list(request):
    products = Product.objects.all()
    return render(request, 'delete_product_list.html', {'products': products})

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('user_dashboard') 
    else:
        form = ReviewForm()

    return render(request, 'add_review.html', {'form': form, 'product': product})