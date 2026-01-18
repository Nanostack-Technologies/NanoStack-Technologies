from django import forms
from ckeditor.widgets import CKEditorWidget
from core.models import Project, BlogPost, JobOpening, Service

class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ProjectForm(BootstrapFormMixin, forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Project
        fields = '__all__'

class BlogPostForm(BootstrapFormMixin, forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = BlogPost
        fields = '__all__'

class JobOpeningForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = JobOpening
        fields = '__all__'

class ServiceForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
