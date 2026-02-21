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

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
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

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
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

import re

def is_spam(data):
    """
    Service to check if a contact message is likely spam.
    """
    email = data.get('email', '').lower()
    name = data.get('name', '').lower()
    subject = data.get('subject', '').lower()
    message = data.get('message', '').lower()
    honeypot = data.get('website', '') # Honeypot field name

    # 1. Honeypot check: If the hidden 'website' field is filled, it's a bot.
    if honeypot:
        return True

    # 2. Blocklist check
    blocked_emails = [
        'xrumer23Acatt@gmail.com',
        'xrumer', # Any email containing xrumer
    ]
    for blocked in blocked_emails:
        if blocked.lower() in email:
            return True

    # 3. Language check: Block Cyrillic (Russian/Bulgarian etc.) characters
    # Since NanoStack is an Indian tech agency, Russian messages are almost certainly spam.
    if re.search('[\u0400-\u04FF]', message) or re.search('[\u0400-\u04FF]', subject):
        return True

    # 4. Common spam patterns
    spam_patterns = [
        r'http://\S+\.ru', # Russian links
        r'https://\S+\.ru',
        r'order a bouquet', # From user's screenshot
        r'заказать букет', # "Order a bouquet" in Russian
    ]
    for pattern in spam_patterns:
        if re.search(pattern, message, re.IGNORECASE) or re.search(pattern, subject, re.IGNORECASE):
            return True

    return False

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def contact(request):
    if request.method == 'POST':
        if is_spam(request.POST):
            # Silently "succeed" for bots so they don't know they were caught
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        ip = get_client_ip(request)
        
        ContactMessage.objects.create(
            name=name, email=email, phone=phone, subject=subject, message=message, ip_address=ip
        )
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')
        
    return render(request, 'core/contact.html', {
        'seo_title': 'Contact NanoStack | Web Development Quote',
        'seo_description': 'Get in touch with NanoStack Technologies for your next project. We offer free consultation for web development and automation services.',
        'seo_keywords': 'Contact NanoStack, Hire Developers, Web Dev Quote, Automation Consulatation'
    })

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

def custom_404(request, exception):
    return render(request, '404.html', status=404)

@csrf_exempt
def contact_api(request):
    if request.method == 'POST':
        # Handle both JSON and Form Data
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
        else:
            data = request.POST

        if is_spam(data):
            # Silently return success to the bot
            return JsonResponse({'message': 'Message sent successfully'}, status=201)

        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone', '')
        subject = data.get('subject')
        message = data.get('message')
        ip = get_client_ip(request)

        if not all([name, email, subject, message]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        ContactMessage.objects.create(
            name=name, email=email, phone=phone, subject=subject, message=message, ip_address=ip
        )

        
        # If standard form submit, verify if they want redirect or JSON
        if request.content_type != 'application/json' and not request.headers.get('x-requested-with') == 'XMLHttpRequest':
             # Optional: Redirect to a 'thank you' page if it's a direct HTML form post
             # For now, returning JSON is safer for an "API"
             pass

        return JsonResponse({'message': 'Message sent successfully'}, status=201)
        
    return JsonResponse({'error': 'Invalid request method'}, status=405)
