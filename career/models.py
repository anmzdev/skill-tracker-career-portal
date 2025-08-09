from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class CareerPath(models.Model):
     name = models.CharField(max_length=100)
     description = models.TextField()

     def __str__(self):
         return self.name

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    career = models.ForeignKey(CareerPath, on_delete=models.CASCADE)



class Skill(models.Model):
    career = models.ForeignKey(CareerPath, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.career.name})"

class UserProfile(models.Model):
    EDUCATION_CHOICES = [
        ('High School', 'High School'),
        ('Diploma', 'Diploma'),
        ('Bachelor', 'Bachelor'),
        ('Master', 'Master'),
        ('PhD', 'PhD'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Student', 'Student'),
        ('Fresher', 'Fresher'),
        ('Employed', 'Employed'),
        ('Job Seeker', 'Job Seeker'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_recruiter = models.BooleanField(default=False)
    name = models.CharField(max_length=100, null=True)  # Allow null
    age = models.PositiveIntegerField(null=True)        # Allow null
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
                              blank=True, null=True)
    education_level = models.CharField(max_length=50, choices=EDUCATION_CHOICES, null=True, blank=True)
    current_status = models.CharField(max_length=50, choices=STATUS_CHOICES, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    chosen_career = models.ForeignKey(CareerPath, on_delete=models.SET_NULL, null=True, blank=True)


BADGE_CHOICES = [
    ('starter', 'Just Started'),
    ('progressing', 'In Progress'),
    ('advanced', 'Practicing'),
    ('completed', 'Completed'),
]

class SkillProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
    badge = models.CharField(max_length=20, choices=BADGE_CHOICES, default='starter')


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    reply = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    company_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.company_name


class JobPost(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    career = models.ForeignKey(CareerPath, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    qualifications = models.TextField(blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Applied')  # Optional status

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"


