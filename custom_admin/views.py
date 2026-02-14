from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
import json
from decimal import Decimal

from core.models import Project, BlogPost, JobOpening, Service, ContactMessage, Client, ClientProject
from .forms import ProjectForm, BlogPostForm, JobOpeningForm, ServiceForm, ClientForm, ClientProjectForm

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
        'clients': Client.objects.count(),
        'client_projects': ClientProject.objects.count(),
    }
    recent_messages = ContactMessage.objects.order_by('-created_at')[:5]

    # Financial summary
    total_revenue = ClientProject.objects.aggregate(total=Sum('total_bill'))['total'] or 0
    total_paid = ClientProject.objects.aggregate(total=Sum('amount_paid'))['total'] or 0
    total_expenses = ClientProject.objects.aggregate(total=Sum('expenses'))['total'] or 0
    total_profit = total_paid - total_expenses

    return render(request, 'custom_admin/dashboard.html', {
        'counts': counts,
        'recent_messages': recent_messages,
        'total_revenue': total_revenue,
        'total_paid': total_paid,
        'total_expenses': total_expenses,
        'total_profit': total_profit,
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


# ========================================
# --- Clients ---
# ========================================

@login_required
@user_passes_test(lambda u: u.is_superuser)
def clients_list(request):
    clients = Client.objects.all().order_by('-created_at')
    return render(request, 'custom_admin/clients/list.html', {'clients': clients})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    projects = client.client_projects.all()
    total_bill = projects.aggregate(total=Sum('total_bill'))['total'] or 0
    total_paid = projects.aggregate(total=Sum('amount_paid'))['total'] or 0
    total_expenses = projects.aggregate(total=Sum('expenses'))['total'] or 0
    total_profit = total_paid - total_expenses
    return render(request, 'custom_admin/clients/detail.html', {
        'client': client,
        'projects': projects,
        'total_bill': total_bill,
        'total_paid': total_paid,
        'total_expenses': total_expenses,
        'total_profit': total_profit,
    })

class ClientCreateView(SuperUserRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'custom_admin/clients/form.html'
    success_url = reverse_lazy('admin_clients_list')

class ClientUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'custom_admin/clients/form.html'
    success_url = reverse_lazy('admin_clients_list')

class ClientDeleteView(SuperUserRequiredMixin, DeleteView):
    model = Client
    template_name = 'custom_admin/clients/confirm_delete.html'
    success_url = reverse_lazy('admin_clients_list')


# ========================================
# --- Client Projects ---
# ========================================

@login_required
@user_passes_test(lambda u: u.is_superuser)
def client_projects_list(request):
    projects = ClientProject.objects.select_related('client').all()
    total_bill = projects.aggregate(total=Sum('total_bill'))['total'] or 0
    total_paid = projects.aggregate(total=Sum('amount_paid'))['total'] or 0
    total_expenses = projects.aggregate(total=Sum('expenses'))['total'] or 0
    total_profit = total_paid - total_expenses
    return render(request, 'custom_admin/client_projects/list.html', {
        'projects': projects,
        'total_bill': total_bill,
        'total_paid': total_paid,
        'total_expenses': total_expenses,
        'total_profit': total_profit,
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def client_project_detail(request, pk):
    project = get_object_or_404(ClientProject.objects.select_related('client'), pk=pk)
    return render(request, 'custom_admin/client_projects/detail.html', {'project': project})

class ClientProjectCreateView(SuperUserRequiredMixin, CreateView):
    model = ClientProject
    form_class = ClientProjectForm
    template_name = 'custom_admin/client_projects/form.html'
    success_url = reverse_lazy('admin_client_projects_list')

class ClientProjectUpdateView(SuperUserRequiredMixin, UpdateView):
    model = ClientProject
    form_class = ClientProjectForm
    template_name = 'custom_admin/client_projects/form.html'
    success_url = reverse_lazy('admin_client_projects_list')

class ClientProjectDeleteView(SuperUserRequiredMixin, DeleteView):
    model = ClientProject
    template_name = 'custom_admin/client_projects/confirm_delete.html'
    success_url = reverse_lazy('admin_client_projects_list')


# ========================================
# --- Analytics API (JSON) ---
# ========================================

@login_required
@user_passes_test(lambda u: u.is_superuser)
def analytics_page(request):
    return render(request, 'custom_admin/analytics.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def analytics_data(request):
    """Returns JSON data for charts on the analytics page."""
    # Monthly revenue & expenses
    monthly = (
        ClientProject.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(
            revenue=Sum('total_bill'),
            paid=Sum('amount_paid'),
            expenses=Sum('expenses'),
        )
        .order_by('month')
    )
    months = []
    revenue_data = []
    expenses_data = []
    profit_data = []
    for m in monthly:
        months.append(m['month'].strftime('%b %Y') if m['month'] else 'N/A')
        revenue_data.append(float(m['revenue'] or 0))
        expenses_data.append(float(m['expenses'] or 0))
        profit_data.append(float((m['paid'] or 0) - (m['expenses'] or 0)))

    # Status distribution
    statuses = (
        ClientProject.objects
        .values('status')
        .annotate(count=Count('id'))
        .order_by('status')
    )
    status_labels = [s['status'] for s in statuses]
    status_counts = [s['count'] for s in statuses]

    # Payment method distribution
    payments = (
        ClientProject.objects
        .values('payment_method')
        .annotate(count=Count('id'))
        .order_by('payment_method')
    )
    payment_labels = [p['payment_method'] for p in payments]
    payment_counts = [p['count'] for p in payments]

    return JsonResponse({
        'months': months,
        'revenue': revenue_data,
        'expenses': expenses_data,
        'profit': profit_data,
        'status_labels': status_labels,
        'status_counts': status_counts,
        'payment_labels': payment_labels,
        'payment_counts': payment_counts,
    })
