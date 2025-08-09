from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(Question)
admin.site.register(Option)
admin.site.register(CareerPath)
admin.site.register(Skill)
admin.site.register(UserProfile)
admin.site.register(SkillProgress)


admin.site.register(JobPost)
admin.site.register(JobApplication)
