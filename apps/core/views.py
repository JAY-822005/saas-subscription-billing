from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta

from apps.users.models import User
from apps.organizations.models import Organization
from apps.subscriptions.models import Subscription
from apps.invoices.models import Invoice


@require_http_methods(["GET", "POST"])
def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect("dashboard")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.email}!")
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid email or password")
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
    
    return render(request, "auth/login.html")


@require_http_methods(["GET", "POST"])
def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect("dashboard")
    
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")
        
        # Validation
        if password != password_confirm:
            messages.error(request, "Passwords do not match")
            return render(request, "auth/register.html")
        
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long")
            return render(request, "auth/register.html")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, "auth/register.html")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return render(request, "auth/register.html")
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role="member"
        )
        
        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")
    
    return render(request, "auth/register.html")


@login_required(login_url="login")
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, "You have been logged out successfully")
    return redirect("login")


@login_required(login_url="login")
def dashboard_view(request):
    """Dashboard view"""
    user = request.user
    
    # Get statistics
    organizations_count = Organization.objects.filter(owner=user).count()
    subscriptions_count = Subscription.objects.filter(
        organization__owner=user,
        status="active"
    ).count()
    invoices_count = Invoice.objects.filter(
        organization__owner=user
    ).count()
    total_revenue = Invoice.objects.filter(
        organization__owner=user,
        status="paid"
    ).aggregate(total=Sum("amount"))["total"] or 0
    
    # Get recent data
    recent_invoices = Invoice.objects.filter(
        organization__owner=user
    ).order_by("-created_at")[:5]
    
    recent_subscriptions = Subscription.objects.filter(
        organization__owner=user,
        status__in=["active", "trial"]
    ).order_by("-created_at")[:5]
    
    context = {
        "organizations_count": organizations_count,
        "subscriptions_count": subscriptions_count,
        "invoices_count": invoices_count,
        "total_revenue": total_revenue,
        "recent_invoices": recent_invoices,
        "recent_subscriptions": recent_subscriptions,
    }
    
    return render(request, "dashboard/index.html", context)


@login_required(login_url="login")
def organizations_list_view(request):
    """List organizations"""
    organizations = Organization.objects.filter(owner=request.user).order_by("-created_at")
    
    context = {
        "organizations": organizations,
    }
    
    return render(request, "dashboard/organizations_list.html", context)


@login_required(login_url="login")
def subscriptions_list_view(request):
    """List subscriptions"""
    subscriptions = Subscription.objects.filter(
        organization__owner=request.user
    ).select_related("organization", "plan").order_by("-created_at")
    
    # Filter by status if provided
    status = request.GET.get("status")
    if status:
        subscriptions = subscriptions.filter(status=status)
    
    context = {
        "subscriptions": subscriptions,
    }
    
    return render(request, "dashboard/subscriptions_list.html", context)


@login_required(login_url="login")
def invoices_list_view(request):
    """List invoices"""
    invoices = Invoice.objects.filter(
        organization__owner=request.user
    ).select_related("organization", "subscription").order_by("-created_at")
    
    # Filter by status if provided
    status = request.GET.get("status")
    if status:
        invoices = invoices.filter(status=status)
    
    context = {
        "invoices": invoices,
    }
    
    return render(request, "dashboard/invoices_list.html", context)


@login_required(login_url="login")
def profile_view(request):
    """User profile view"""
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.phone = request.POST.get("phone", user.phone)
        user.save()
        messages.success(request, "Profile updated successfully")
        return redirect("profile")
    
    return render(request, "dashboard/profile.html")
