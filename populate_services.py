import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NanoStack_Technologies.settings')
django.setup()

from core.models import Service

services_data = [
    {
        "title": "Web Development",
        "description": "Custom websites built with modern technologies ensuring speed, security, and scalability.",
        "icon": "fas fa-code",
        "order": 1
    },
    {
        "title": "Web Design",
        "description": "UI/UX designs that are visually stunning and user-centric.",
        "icon": "fas fa-paint-brush",
        "order": 2
    },
    {
        "title": "Custom Software",
        "description": "Tailored software solutions to solve complex business problems.",
        "icon": "fas fa-laptop-code",
        "order": 3
    },
    {
        "title": "CMS Development",
        "description": "Manage your content easily with custom CMS solutions.",
        "icon": "fas fa-cogs",
        "order": 4
    },
    {
        "title": "API Integration",
        "description": "Seamlessly connect your systems with robust API integrations.",
        "icon": "fas fa-network-wired",
        "order": 5
    },
    {
        "title": "Automations",
        "description": "Streamline workflows with N8N and custom automation scripts.",
        "icon": "fas fa-robot",
        "order": 6
    },
    {
        "title": "WhatsApp Integration",
        "description": "Engage customers directly through WhatsApp automation.",
        "icon": "fab fa-whatsapp",
        "order": 7
    },
    {
        "title": "App Development",
        "description": "Native and cross-platform mobile applications.",
        "icon": "fas fa-mobile-alt",
        "order": 8
    }
]

for data in services_data:
    Service.objects.get_or_create(title=data['title'], defaults=data)
    print(f"Created/Checked service: {data['title']}")
