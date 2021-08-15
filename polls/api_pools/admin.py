from django.contrib import admin
from .models import Poll, Question, Answer, ResponseContent


class AdminPoll(admin.ModelAdmin):
    list_display = ['id', 'title', 'end_date']
    list_display_links = ['title']


class AdminQuestion(admin.ModelAdmin):
    list_display = ['id', 'text', 'poll', 'type_question']
    list_display_links = ['text']


class AdminResponseContent(admin.ModelAdmin):
    list_display = ['id','question', 'option']
    list_display_links = ['question']

admin.site.register(Poll, AdminPoll)
admin.site.register(Question, AdminQuestion)
admin.site.register(Answer)
admin.site.register(ResponseContent,AdminResponseContent)
