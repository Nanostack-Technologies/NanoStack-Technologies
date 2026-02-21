from django.contrib import admin
from .models import Project, BlogPost, JobOpening, ContactMessage, Service

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'tech_stack', 'client_location', 'duration', 'created_at')
    search_fields = ('title', 'tech_stack', 'description')
    list_filter = ('created_at',)
    prepopulated_fields = {'slug': ('title',)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'author')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'type', 'posted_at')
    search_fields = ('title', 'location', 'description')
    list_filter = ('type', 'location', 'posted_at')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'ip_address', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message', 'ip_address')
    list_filter = ('created_at',)
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'ip_address', 'created_at')

    def has_add_permission(self, request):
        return False

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'description')
