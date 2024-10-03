from django.db import models
from django.contrib.auth.models import User # user使用者
# Create your models here.

# Task任務
class Task(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    priority = models.IntegerField()
    status = models.CharField(max_length=50)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
# SharedTask
class SharedTask(models.Model):
    id = models.IntegerField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.task.title} shared with {self.user.username}"

# Comment
class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.task.title}"

class ActivityLog(models.Model):
    id = models.IntegerField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    action_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} by {self.user.username} on {self.task.title}"
