from django.contrib import admin
from .models import Task, SharedTask, Comment, ActivityLog
# Register your models here.

table = [Task, SharedTask, Comment, ActivityLog]

for i in table:
    admin.site.register(i)