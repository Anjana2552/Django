from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import  login, logout
from .forms import LoginForm,ProductForm, ReviewForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from .models import Like, Product, Review, ReviewReply
from django.db.models import Avg
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
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
        if user.is_admin:
            messages.error(request, "Admins must log in through the admin login page.")
            return redirect('login') 
        login(request, user)
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

def view_reviews(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.select_related('user').prefetch_related('likes')

    # Calculate average rating
    avg_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']

    user_liked_review_ids = set()
    if request.user.is_authenticated:
        user_liked_review_ids = set(
            Like.objects.filter(user=request.user, review__in=reviews).values_list('review_id', flat=True)
        )

    for review in reviews:
        review.liked_by_user = review.id in user_liked_review_ids

    context = {
        'product': product, 
        'reviews': reviews,
        'avg_rating': avg_rating,
    }
    
    return render(request, 'view_reviews.html', context)


@login_required
def toggle_like(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    like, created = Like.objects.get_or_create(user=request.user, review=review)
    if not created:
        like.delete() 
    return redirect('view_reviews', product_id=review.product.id)

@login_required
def add_reply(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(Review, id=review_id)
        comment = request.POST.get('comment')
        if comment:
            ReviewReply.objects.create(review=review, user=request.user, comment=comment)
    return redirect('view_reviews', product_id=review.product.id)

def landing_page(request):
    return render(request, 'landing.html')

@login_required
def like_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    Like.objects.get_or_create(review=review, user=request.user)
    # Check if coming from product detail page
    if 'product_detail' in request.META.get('HTTP_REFERER', ''):
        return redirect('product_detail', product_id=review.product.id)
    return redirect('view_reviews', product_id=review.product.id)

@login_required
def dislike_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    Like.objects.filter(review=review, user=request.user).delete()
    # Check if coming from product detail page
    if 'product_detail' in request.META.get('HTTP_REFERER', ''):
        return redirect('product_detail', product_id=review.product.id)
    return redirect('view_reviews', product_id=review.product.id)

def admin_login_view(request):
    form = AuthenticationForm(data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        if user.is_admin:  
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "You are not authorized to access the admin dashboard.")
            return redirect('admin_login')

    return render(request, 'admin_login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.select_related('user').prefetch_related('likes', 'replies')
    
    # Calculate average rating
    avg_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
    
    # Get rating distribution
    rating_counts = {}
    for i in range(1, 6):
        rating_counts[i] = reviews.filter(rating=i).count()
    
    total_reviews = reviews.count()
    
    # Calculate rating percentages
    rating_percentages = {}
    for rating, count in rating_counts.items():
        rating_percentages[rating] = (count / total_reviews * 100) if total_reviews > 0 else 0
    
    # Get user's like status for reviews if authenticated
    user_liked_review_ids = set()
    if request.user.is_authenticated:
        user_liked_review_ids = set(
            Like.objects.filter(user=request.user, review__in=reviews).values_list('review_id', flat=True)
        )
    
    for review in reviews:
        review.liked_by_user = review.id in user_liked_review_ids
    
    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'total_reviews': total_reviews,
        'rating_counts': rating_counts,
        'rating_percentages': rating_percentages,
        # Add individual rating data for easier template access
        'rating_5_percentage': rating_percentages.get(5, 0),
        'rating_4_percentage': rating_percentages.get(4, 0),
        'rating_3_percentage': rating_percentages.get(3, 0),
        'rating_2_percentage': rating_percentages.get(2, 0),
        'rating_1_percentage': rating_percentages.get(1, 0),
        'rating_5_count': rating_counts.get(5, 0),
        'rating_4_count': rating_counts.get(4, 0),
        'rating_3_count': rating_counts.get(3, 0),
        'rating_2_count': rating_counts.get(2, 0),
        'rating_1_count': rating_counts.get(1, 0),
    }
    
    return render(request, 'product_detail.html', context)

def google_oauth_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if email:
            # Extract username from email (part before @)
            username = email.split('@')[0]
            
            # Try to find existing user by email first (get the first one if multiple exist)
            user = User.objects.filter(email=email).first()
            
            if not user:
                # Try to find by username if no user found by email
                user = User.objects.filter(username=username).first()
                
                if user:
                    # Update email if user exists but doesn't have this email
                    if not user.email:
                        user.email = email
                        user.save()
                else:
                    # Create new user with unique username
                    # Check if username already exists and create a unique one
                    original_username = username
                    counter = 1
                    while User.objects.filter(username=username).exists():
                        username = f"{original_username}_{counter}"
                        counter += 1
                    
                    # Create new user with email as username
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=None,  # Google OAuth users don't need password
                        role='user'  # Default role is user
                    )
                    user.assign_group()
            
            # Log in the user with explicit backend
            from django.contrib.auth import login
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            # Redirect based on user role
            if user.is_admin:
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
    
    # If something goes wrong, redirect back to login
    return redirect('login')