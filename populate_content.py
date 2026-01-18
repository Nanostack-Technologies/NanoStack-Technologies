import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NanoStack_Technologies.settings')
django.setup()

from core.models import Project, BlogPost, JobOpening

# Projects Data
projects_data = [
    {
        "title": "EcoTrack - Sustainable Supply Chain Platform",
        "description": "A comprehensive SaaS solution designed for logistics companies to monitor and reduce their carbon footprint. \n\nKey features include real-time emission tracking, AI-powered route optimization, and automated sustainability reporting. This project involved complex data visualization and integration with IoT devices on fleet vehicles. \n\nThe system handles millions of data points daily and provides actionable insights to help businesses achieve their green goals.",
        "image": "projects/project1.jpg",
        "tech_stack": "Python, Django, React, PostgreSQL, Docker",
        "link": "https://example.com/ecotrack"
    },
    {
        "title": "FinSight - AI Financial Analytics",
        "description": "An advanced financial dashboard providing real-time market analysis and portfolio management. \n\nLeveraging machine learning algorithms, FinSight predicts market trends and offers personalized investment recommendations. It features a high-frequency trading engine and secure bank-level encryption for user data. \n\nBuilt for speed and security, it serves thousands of active traders.",
        "image": "projects/project2.jpg",
        "tech_stack": "Node.js, Next.js, TensorFlow, MongoDB",
        "link": "https://example.com/finsight"
    },
    {
        "title": "MediConnect - Telemedicine App",
        "description": "A cross-platform mobile application connecting patients with healthcare providers securely. \n\nFeatures include video consultations, e-prescriptions, and appointment scheduling. The app is fully HIPAA compliant and integrates with major insurances providers. \n\nWe focused heavily on the user experience to ensure accessibility for elderly patients.",
        "image": "projects/project3.jpg",
        "tech_stack": "Flutter, Firebase, FastApi, WebRTC",
        "link": "https://example.com/mediconnect"
    }
]

# Blog Data
blog_data = [
    {
        "title": "The Future of Web Automation with Python",
        "content": "Automation is no longer just a buzzword; it's a necessity for modern businesses. In this post, we dive deep into how Python is leading the charge in web automation. \n\nFrom scraping complex data sets to automating repetitive testing workflows, Python libraries like Selenium, Beautiful Soup, and Playwright are changing the game. \n\nWe explore real-world use cases where automation saved companies hundreds of man-hours per month and significantly reduced human error. Learn how to get started with your first automation script today.",
        "image": "blog/blog1.jpg",
        "author": "Pavan Mehta"
    },
    {
        "title": "Why Your Business Needs a Custom CRM in 2024",
        "content": "Off-the-shelf CRM solutions like Salesforce are powerful, but they often come with unnecessary bloat and high costs. \n\nA custom CRM, tailored specifically to your business processes, can streamline operations and improve team efficiency. \n\nIn this article, we discuss the benefits of building a bespoke CRM using Django. We cover data ownership, custom integrations with your existing tools, and the long-term ROI of investing in your own software infrastructure.",
        "image": "blog/blog2.jpg",
        "author": "Nakul Talsaniya"
    },
    {
        "title": "Scaling Django Applications for High Traffic",
        "content": "Django is known for its 'batteries-included' approach, but how does it hold up under heavy load? \n\nThe answer is: exceptionally well, if architected correctly. \n\nWe share our internal best practices for scaling Django apps. Topics include database optimization and indexing, using Redis for caching, asynchronous task queues with Celery, and load balancing strategies. Whether you're a startup expecting a spike or an enterprise, these tips will keep your server humming.",
        "image": "blog/blog3.jpg",
        "author": "Nakul Talsaniya"
    }
]

# Job Data
job_data = [
    {
        "title": "Senior Python Developer",
        "description": "We are looking for an experienced Python developer to join our backend team. You will be responsible for building scalable APIs and microservices. \n\nResponsibilities:\n- Design and implement robust APIs using Django/FastAPI.\n- Optimize database queries and schema design.\n- Collaborate with frontend teams to integrate user-facing elements.\n- Mentor junior developers.",
        "requirements": "- 4+ years of experience with Python.\n- Strong knowledge of Django or Flask.\n- Experience with PostgreSQL and Redis.\n- Familiarity with Docker and CI/CD pipelines.",
        "location": "Remote / Ahmedabad",
        "type": "Full Time"
    },
    {
        "title": "Frontend Engineer (React/Next.js)",
        "description": "Join our creative team to build beautiful, responsive web interfaces. You will work closely with designers to bring high-fidelity mockups to life. \n\nResponsibilities:\n- Develop new user-facing features using React.js.\n- Build reusable components and front-end libraries.\n- Ensure technical feasibility of UI/UX designs.\n- Optimize application for maximum speed and scalability.",
        "requirements": "- 3+ years of experience with React.js and Next.js.\n- Strong proficiency in JavaScript/TypeScript, CSS, and HTML.\n- Experience with state management tools (Redux/Zustand).\n- Eye for detail and design aesthetics.",
        "location": "Ahmedabad",
        "type": "Full Time"
    }
]

print("Starting population script...")

# Populate Projects
for p_data in projects_data:
    obj, created = Project.objects.get_or_create(
        title=p_data['title'],
        defaults=p_data
    )
    if created:
        print(f"Created Project: {obj.title}")
    else:
        print(f"Project already exists: {obj.title}")

# Populate Blogs
for b_data in blog_data:
    obj, created = BlogPost.objects.get_or_create(
        title=b_data['title'],
        defaults=b_data
    )
    if created:
        print(f"Created Blog: {obj.title}")
    else:
        print(f"Blog already exists: {obj.title}")

# Populate Jobs
for j_data in job_data:
    obj, created = JobOpening.objects.get_or_create(
        title=j_data['title'],
        defaults=j_data
    )
    if created:
        print(f"Created Job: {obj.title}")
    else:
        print(f"Job already exists: {obj.title}")

print("Population complete!")
