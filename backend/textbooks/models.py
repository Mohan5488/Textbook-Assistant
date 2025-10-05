from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    READING_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('regular', 'Regular'),
        ('advanced', 'Advanced'),
    ]
    reading_level = models.CharField(max_length=20, choices=READING_LEVEL_CHOICES, default='beginner')
    prefs = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"


class Document(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    doc_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.title


class Topic(models.Model):
    topic_id = models.AutoField(primary_key=True)
    doc = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="topics")
    title = models.CharField(max_length=255)
    page_start = models.IntegerField()
    page_end = models.IntegerField()
    prerequisites = models.JSONField(default=list)
    summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} (Doc: {self.doc.title})"


class SubTopic(models.Model):
    subtopic_id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="subtopics")
    title = models.CharField(max_length=255)
    page_start = models.IntegerField(null=True, blank=True)
    page_end = models.IntegerField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} (Topic: {self.topic.title})"


class Chunk(models.Model):
    chunk_id = models.AutoField(primary_key=True)
    doc = models.ForeignKey(Document, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    subtopic = models.ForeignKey(SubTopic, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    embedding_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"Chunk {self.chunk_id} - Doc {self.doc_id}"
