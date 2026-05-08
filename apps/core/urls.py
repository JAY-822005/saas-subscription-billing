from django.urls import path
from . import views

urlpatterns = [
    # Auth URLs
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    
    # Dashboard URLs
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("profile/", views.profile_view, name="profile"),
    
    # Organization URLs
    path("organizations/", views.organizations_list_view, name="organizations_list"),
    
    # Subscription URLs
    path("subscriptions/", views.subscriptions_list_view, name="subscriptions_list"),
    
    # Invoice URLs
    path("invoices/", views.invoices_list_view, name="invoices_list"),
]
