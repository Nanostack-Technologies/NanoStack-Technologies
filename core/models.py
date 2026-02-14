from django.db import models

from django.utils.text import slugify

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=200, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    tech_stack = models.CharField(max_length=200, help_text="Comma separated technologies")
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=200, null=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/')
    author = models.CharField(max_length=100, default="Admin")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class JobOpening(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=[('Full Time', 'Full Time'), ('Part Time', 'Part Time'), ('Contract', 'Contract')])
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="FontAwesome class (e.g., 'fas fa-code')")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Client(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def total_projects(self):
        return self.client_projects.count()

    def total_revenue(self):
        return sum(p.total_bill for p in self.client_projects.all())


class ClientProject(models.Model):
    STATUS_CHOICES = [
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Delivered', 'Delivered'),
        ('On Hold', 'On Hold'),
        ('Cancelled', 'Cancelled'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('Bank Transfer', 'Bank Transfer'),
        ('UPI', 'UPI'),
        ('Cash', 'Cash'),
        ('PayPal', 'PayPal'),
        ('Cheque', 'Cheque'),
        ('Other', 'Other'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_projects')
    project_name = models.CharField(max_length=300)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='In Progress')
    tech_stack = models.CharField(max_length=500, help_text="Comma separated technologies", blank=True)
    description = models.TextField(blank=True)
    total_bill = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, default='Bank Transfer')
    expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Total expenses for this project")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    delivered_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project_name} — {self.client.name}"

    @property
    def balance_due(self):
        return self.total_bill - self.amount_paid

    @property
    def profit_or_loss(self):
        return self.amount_paid - self.expenses

    @property
    def is_profitable(self):
        return self.profit_or_loss >= 0

    class Meta:
        ordering = ['-created_at']
