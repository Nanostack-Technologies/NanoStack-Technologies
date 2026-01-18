from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from core.models import Project, BlogPost, JobOpening, Service, ContactMessage
from .forms import ProjectForm, BlogPostForm, JobOpeningForm, ServiceForm

# --- Authentication ---

def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Access denied. Admin only.")
    else:
        form = AuthenticationForm()
    return render(request, 'custom_admin/login.html', {'form': form})

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

# --- Mixins ---

class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

# --- Dashboard ---

@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    counts = {
        'projects': Project.objects.count(),
        'blogs': BlogPost.objects.count(),
        'services': Service.objects.count(),
        'jobs': JobOpening.objects.count(),
        'messages': ContactMessage.objects.count(),
    }
    recent_messages = ContactMessage.objects.order_by('-created_at')[:5]
    return render(request, 'custom_admin/dashboard.html', {
        'counts': counts,
        'recent_messages': recent_messages
    })

# --- Projects ---

@login_required
@user_passes_test(lambda u: u.is_superuser)
def projects_list(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'custom_admin/projects/list.html', {'projects': projects})

class ProjectCreateView(SuperUserRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'custom_admin/projects/form.html'
    success_url = reverse_lazy('admin_projects_list')

class ProjectUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'custom_admin/projects/form.html'
    success_url = reverse_lazy('admin_projects_list')

class ProjectDeleteView(SuperUserRequiredMixin, DeleteView):
    model = Project
    template_name = 'custom_admin/projects/confirm_delete.html'
    success_url = reverse_lazy('admin_projects_list')

# --- Blogs ---

@login_required
@user_passes_test(lambda u: u.is_superuser)
def blogs_list(request):
    blogs = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'custom_admin/blog/list.html', {'blogs': blogs})

class BlogCreateView(SuperUserRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'custom_admin/blog/form.html'
    success_url = reverse_lazy('admin_blogs_list')

class BlogUpdateView(SuperUserRequiredMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'custom_admin/blog/form.html'
    success_url = reverse_lazy('admin_blogs_list')

class BlogDeleteView(SuperUserRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'custom_admin/blog/confirm_delete.html'
    success_url = reverse_lazy('admin_blogs_list')

# --- Services ---

@login_required
@user_passes_test(lambda u: u.is_superuser)
def services_list(request):
    services = Service.objects.all().order_by('order')
    return render(request, 'custom_admin/services/list.html', {'services': services})

class ServiceCreateView(SuperUserRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'custom_admin/services/form.html'
    success_url = reverse_lazy('admin_services_list')

class ServiceUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'custom_admin/services/form.html'
    success_url = reverse_lazy('admin_services_list')

class ServiceDeleteView(SuperUserRequiredMixin, DeleteView):
    model = Service
    template_name = 'custom_admin/services/confirm_delete.html'
    success_url = reverse_lazy('admin_services_list')

# --- Jobs ---

@login_required
@user_passes_test(lambda u: u.is_superuser)
def jobs_list(request):
    jobs = JobOpening.objects.all().order_by('-posted_at')
    return render(request, 'custom_admin/jobs/list.html', {'jobs': jobs})

class JobCreateView(SuperUserRequiredMixin, CreateView):
    model = JobOpening
    form_class = JobOpeningForm
    template_name = 'custom_admin/jobs/form.html'
    success_url = reverse_lazy('admin_jobs_list')

class JobUpdateView(SuperUserRequiredMixin, UpdateView):
    model = JobOpening
    form_class = JobOpeningForm
    template_name = 'custom_admin/jobs/form.html'
    success_url = reverse_lazy('admin_jobs_list')

class JobDeleteView(SuperUserRequiredMixin, DeleteView):
    model = JobOpening
    template_name = 'custom_admin/jobs/confirm_delete.html'
    success_url = reverse_lazy('admin_jobs_list')

# --- Messages ---

@login_required
@user_passes_test(lambda u: u.is_superuser)
def messages_list(request):
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'custom_admin/messages/list.html', {'messages_list': messages_list})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def message_detail(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    return render(request, 'custom_admin/messages/detail.html', {'msg': msg})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def message_delete(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        msg.delete()
        messages.success(request, 'Message deleted.')
        return redirect('admin_messages_list')
    return render(request, 'custom_admin/messages/confirm_delete.html', {'object': msg})
