from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, BlogPostForm
from django.contrib.auth.decorators import login_required
from .models import BlogPost, CATEGORY_CHOICES

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == 'doctor':
                return redirect('doctor_dashboard')
            else:
                return redirect('patient_dashboard')
        else:
            error = "Invalid username or password" 
    return render(request, 'login.html', {'error': error})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def home_view(request):
    return render(request, 'home.html')

@login_required
def doctor_dashboard(request):
    if request.user.user_type != 'doctor':
        return redirect('unauthorized')

    selected_category = request.GET.get('category', 'All')

    if selected_category == 'All':
        blogs = BlogPost.objects.filter(doctor=request.user).order_by('-created_at')
    else:
        blogs = BlogPost.objects.filter(doctor=request.user, category=selected_category).order_by('-created_at')

    return render(request, 'doctor_dashboard.html', {
        'user': request.user,
        'blogs': blogs,
        'selected_category': selected_category,
        'categories': ['All'] + [c[0] for c in CATEGORY_CHOICES]
    })


@login_required
def patient_dashboard(request):
    if request.user.user_type != 'patient':
        return redirect('unauthorized')

    selected_category = request.GET.get('category', 'All')

    if selected_category == 'All':
        blogs = BlogPost.objects.filter(is_draft=False).order_by('-created_at')
    else:
        blogs = BlogPost.objects.filter(category=selected_category, is_draft=False).order_by('-created_at')

    return render(request, 'patient_dashboard.html', {
        'user': request.user,
        'blogs': blogs,
        'selected_category': selected_category,
        'categories': ['All'] + [c[0] for c in CATEGORY_CHOICES]
    })


@login_required
def create_blog(request):
    if request.user.user_type != 'doctor':
        return redirect('unauthorized')
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.doctor = request.user
            blog.save()
            return redirect('doctor_dashboard')
    else:
        form = BlogPostForm()
    return render(request, 'create_blog.html', {'form': form})

@login_required
def delete_blog(request, blog_id):
    if request.user.user_type != 'doctor':
        return redirect('unauthorized')
    blog = get_object_or_404(BlogPost, id=blog_id, doctor=request.user)
    if request.method == 'POST':
        blog.delete()
        return redirect('doctor_dashboard')
    return render(request, 'confirm_delete.html', {'blog': blog})
@login_required
def edit_blog(request, blog_id):
    if request.user.user_type != 'doctor':
        return redirect('unauthorized')
    
    blog = get_object_or_404(BlogPost, id=blog_id, doctor=request.user)
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('doctor_dashboard')
    else:
        form = BlogPostForm(instance=blog)
    
    return render(request, 'edit_blog.html', {'form': form, 'blog': blog})
@login_required
def blog_detail(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)

    if request.user.user_type == 'patient':
        if blog.is_draft:
            return redirect('unauthorized')  # or show 404
    elif request.user.user_type == 'doctor':
        if blog.doctor != request.user:
            return redirect('unauthorized')
    else:
        return redirect('unauthorized')

    return render(request, 'blog_detail.html', {'blog': blog})
