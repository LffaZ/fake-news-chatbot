from django.db import models
import uuid

# Create your models here.
class UserQuery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    retrieved_docs = models.JSONField(blank=True, null=True)
    label = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.question[:50]
