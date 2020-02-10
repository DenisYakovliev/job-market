from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from accounts.models import User


JOB_TYPE = (
    ('1', "Full time"),
    ('2', "Part time"),
    ('3', "Internship"),
)

CATEGORY = (
    ('1', "Web design"),
    ('2', "Graphic design"),
    ('3', "Web developer"),
    ('4', "Human Resources"),
    ('5', "Software Developer")
)


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, db_index=True, verbose_name='title')
    salary = models.PositiveIntegerField(default=0, blank=True)
    description = models.TextField(max_length=1000)
    location = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=10, blank=True, choices=JOB_TYPE)
    category = models.CharField(max_length=100, blank=True, choices=CATEGORY)
    last_date = models.DateTimeField(null=True)
    website = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)
    views = models.PositiveIntegerField('Просмотры', default=0)  # количество просмотров
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def get_absolute_url(self):
        return reverse('job_detail_url', kwargs={'job_id': self.id})

    def get_update_url(self):
        return reverse('job_update_url', kwargs={'job_id': self.id})

    def get_delete_url(self):
        return reverse('job_delete_url', kwargs={'job_id': self.id})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Jobs"
        ordering = ["-created_at"]


class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicants')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.get_full_name()

