from django.contrib import admin
from .models import Question, Answer, Like
# Register your models here.

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Like)
