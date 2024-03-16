from django.db import models
from accounts.models import User

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=2000)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title