from django.urls import path
from . import views

urlpatterns = [
    path("", views.role_dashboard, name="dashboard"),  # ✅ single entry dashboard redirect

    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("profile/", views.profile_view, name="profile"),

    # User pages
    path("user/dashboard/", views.user_dashboard, name="user_dashboard"),
    path("complaints/submit/", views.submit_complaint, name="submit_complaint"),
    path("complaints/mine/", views.my_complaints, name="my_complaints"),
    path("complaints/<int:pk>/", views.complaint_detail, name="complaint_detail"),
    path("complaints/<int:pk>/edit/", views.edit_complaint, name="edit_complaint"),

    # Admin pages
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-panel/complaints/", views.admin_complaints, name="admin_complaints"),
    path("admin-panel/complaints/<int:pk>/update/", views.admin_update_complaint, name="admin_update_complaint"),
    path("admin-panel/complaints/<int:pk>/delete/", views.admin_delete_complaint, name="admin_delete_complaint"),
]
