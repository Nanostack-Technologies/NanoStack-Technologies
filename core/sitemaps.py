from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Project, BlogPost, JobOpening

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['home', 'about', 'projects', 'blog', 'career', 'contact']

    def location(self, item):
        return reverse(item)

class ProjectSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return Project.objects.all()
        
    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('project_detail', args=[obj.slug])

class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return BlogPost.objects.all()

    def lastmod(self, obj):
        return obj.created_at
    
    def location(self, obj):
        return reverse('blog_detail', args=[obj.slug])
