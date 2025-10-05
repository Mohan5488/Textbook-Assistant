from django.contrib import admin
from .models import Document, Topic, Chunk, SubTopic

admin.site.register(Document)
admin.site.register(Topic)
admin.site.register(Chunk)
admin.site.register(SubTopic)