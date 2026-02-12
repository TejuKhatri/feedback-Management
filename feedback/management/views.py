from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SignupForm, LoginForm, ComplaintForm, AdminUpdateForm, ProfileForm
from .models import Complaint

def is_admin(user):
    return user.is_staff or user.is_superuser

# ✅ single route: decides dashboard based on role
@login_required
def role_dashboard(request):
    if is_admin(request.user):
        return redirect("admin_dashboard")
    return redirect("user_dashboard")

@login_required
def user_dashboard(request):
    # simple user stats
    total = Complaint.objects.filter(user=request.user).count()
    open_count = Complaint.objects.filter(user=request.user, status="open").count()
    progress_count = Complaint.objects.filter(user=request.user, status="in_progress").count()
    resolved_count = Complaint.objects.filter(user=request.user, status="resolved").count()

    return render(request, "complaints/user_dashboard.html", {
        "total": total,
        "open_count": open_count,
        "progress_count": progress_count,
        "resolved_count": resolved_count,
    })

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # admin stats
    total = Complaint.objects.all().count()
    open_count = Complaint.objects.filter(status="open").count()
    progress_count = Complaint.objects.filter(status="in_progress").count()
    resolved_count = Complaint.objects.filter(status="resolved").count()
    latest = Complaint.objects.select_related("user").order_by("-created_at")[:6]

    return render(request, "complaints/admin_dashboard.html", {
        "total": total,
        "open_count": open_count,
        "progress_count": progress_count,
        "resolved_count": resolved_count,
        "latest": latest,
    })

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password1"])
        user.save()
        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")

    return render(request, "auth/signup.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["username"].strip(),
            password=form.cleaned_data["password"]
        )
        if user:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect("dashboard")  # ✅ will auto route to correct dashboard
        messages.error(request, "Invalid username or password.")

    return render(request, "auth/login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")

@login_required
def profile_view(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("profile")
    return render(request, "complaints/profile.html", {"form": form})

# ---------------- Existing complaint views remain same ----------------

@login_required
def submit_complaint(request):
    form = ComplaintForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        c = form.save(commit=False)
        c.user = request.user
        c.save()
        messages.success(request, "Complaint submitted successfully.")
        return redirect("my_complaints")
    return render(request, "complaints/submit.html", {"form": form, "edit_mode": False})

@login_required
def my_complaints(request):
    qs = Complaint.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "complaints/my_complaints.html", {"complaints": qs})

@login_required
def complaint_detail(request, pk):
    c = get_object_or_404(Complaint, pk=pk)
    if c.user != request.user and not is_admin(request.user):
        messages.error(request, "You are not allowed to view this complaint.")
        return redirect("dashboard")
    return render(request, "complaints/detail.html", {"c": c})

@login_required
def edit_complaint(request, pk):
    c = get_object_or_404(Complaint, pk=pk, user=request.user)
    if c.status == "resolved":
        messages.error(request, "You cannot edit after it is resolved.")
        return redirect("complaint_detail", pk=pk)

    form = ComplaintForm(request.POST or None, instance=c)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Complaint updated successfully.")
        return redirect("complaint_detail", pk=pk)

    return render(request, "complaints/submit.html", {"form": form, "edit_mode": True})

@login_required
@user_passes_test(is_admin)
def admin_complaints(request):
    status = request.GET.get("status", "").strip()
    qs = Complaint.objects.all().order_by("-created_at")
    if status in ["open", "in_progress", "resolved"]:
        qs = qs.filter(status=status)
    return render(request, "complaints/admin_list.html", {"complaints": qs, "status": status})

@login_required
@user_passes_test(is_admin)
def admin_update_complaint(request, pk):
    c = get_object_or_404(Complaint, pk=pk)
    form = AdminUpdateForm(request.POST or None, instance=c)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Complaint updated successfully.")
        return redirect("admin_complaints")

    return render(request, "complaints/detail.html", {"c": c, "admin_form": form})

@login_required
@user_passes_test(is_admin)
def admin_delete_complaint(request, pk):
    c = get_object_or_404(Complaint, pk=pk)
    if request.method == "POST":
        c.delete()
        messages.success(request, "Complaint deleted successfully.")
        return redirect("admin_complaints")
    return render(request, "complaints/detail.html", {"c": c, "confirm_delete": True})
