from django import forms
from ckeditor.widgets import CKEditorWidget
from core.models import Project, BlogPost, JobOpening, Service, Client, ClientProject

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

class ClientForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone', 'company', 'address', 'notes']

class ClientProjectForm(BootstrapFormMixin, forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    delivered_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = ClientProject
        fields = ['client', 'project_name', 'status', 'tech_stack', 'description',
                  'total_bill', 'amount_paid', 'payment_method', 'expenses',
                  'start_date', 'end_date', 'delivered_date', 'notes']
