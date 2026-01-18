from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, BlogPost, JobOpening, ContactMessage, Service
from django.contrib import messages

def home(request):
    recent_projects = Project.objects.all().order_by('-created_at')[:3]
    recent_blogs = BlogPost.objects.all().order_by('-created_at')[:3]
    services = Service.objects.all().order_by('order')
    return render(request, 'core/home.html', {
        'recent_projects': recent_projects,
        'recent_blogs': recent_blogs,
        'services': services,
        'seo_title': 'NanoStack Technologies | Transforming Visions into Digital Reality',
    })

def about(request):
    return render(request, 'core/about.html', {
        'seo_title': 'About NanoStack | Top Web Development Agency in India',
        'seo_description': 'Learn about NanoStack Technologies, founded by Pavan Mehta and Nakul Talsaniya. We are a team of expert developers building scalable web and automation solutions.',
        'seo_keywords': 'About NanoStack, Best Web Agency, Software Company Founders, Pavan Mehta, Nakul Talsaniya'
    })

def projects(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'core/projects.html', {
        'projects': projects,
        'seo_title': 'Our Portfolio | Custom Software & Web Projects',
        'seo_description': 'Explore our portfolio of successful projects including EcoTrack, FinSight, and MediConnect. See how we deliver excellence in code.',
        'seo_keywords': 'NanoStack Portfolio, Case Studies, Web Projects, App Development Examples'
    })

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'core/project_detail.html', {
        'project': project,
        'seo_title': f"{project.title} | Case Study by NanoStack",
        'seo_description': project.description[:160],
        'seo_keywords': f"{project.title}, {project.tech_stack}, Software Case Study"
    })

def blog(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'core/blog.html', {
        'posts': posts,
        'seo_title': 'Tech Insights & Blog | NanoStack Technologies',
        'seo_description': 'Read the latest trends in Web Development, Python, Django, and Automation. Expert insights from our tech leads.',
        'seo_keywords': 'Tech Blog, Web Dev Blog, Python Tutorials, Business Automation Tips'
    })

def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'core/blog_detail.html', {
        'post': post,
        'seo_title': f"{post.title} | NanoStack Blog",
        'seo_description': post.content[:160],
        'seo_keywords': f"{post.title}, Tech Article, {post.author}"
    })

def career(request):
    jobs = JobOpening.objects.all().order_by('-posted_at')
    return render(request, 'core/career.html', {
        'jobs': jobs,
        'seo_title': 'Careers at NanoStack | Join Our Team',
        'seo_description': 'Looking for a job in tech? NanoStack is hiring Python Developers, React Engineers, and more. Apply now to build the future.',
        'seo_keywords': 'Tech Jobs, Python Developers Hiring, Remote Jobs, Software Engineer Careers'
    })

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(
            name=name, email=email, phone=phone, subject=subject, message=message
        )
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')
        
    return render(request, 'core/contact.html', {
        'seo_title': 'Contact NanoStack | Web Development Quote',
        'seo_description': 'Get in touch with NanoStack Technologies for your next project. We offer free consultation for web development and automation services.',
        'seo_keywords': 'Contact NanoStack, Hire Developers, Web Dev Quote, Automation Consulatation'
    })

def custom_404(request, exception):
    return render(request, '404.html', status=404)
