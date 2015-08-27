from django.contrib import admin

from .models import Question_Report, Answer_Report, Comment_Report, Profile_Report
# Register your models here.


class Question_ReportAdmin(admin.ModelAdmin):
    readonly_fields = ['timestamp', 'updated', 'classe']
    list_display = ['question', 'user_num', 'status', 'kind']
    list_filter = ['status', 'kind']
    search_fields = ['question__titulo',]
    
    def user_num(self, obj):
        users = []
        for user in obj.from_users.all():
            users.append(user)
        return len(users)
    
    class Meta:
        model = Question_Report

admin.site.register(Question_Report, Question_ReportAdmin)



class Answer_ReportAdmin(admin.ModelAdmin):
    readonly_fields = ['timestamp', 'updated', 'classe']
    list_display = ['answer', 'user_num', 'status', 'kind']
    list_filter = ['status', 'kind']
    search_fields = ['question__titulo',]
    
    def user_num(self, obj):
        users = []
        for user in obj.from_users.all():
            users.append(user)
        return len(users)
    
    class Meta:
        model = Answer_Report

admin.site.register(Answer_Report, Answer_ReportAdmin)



class Comment_ReportAdmin(admin.ModelAdmin):
    readonly_fields = ['timestamp', 'updated', 'classe']
    list_display = ['comment', 'user_num', 'status', 'kind']
    list_filter = ['status', 'kind']
    search_fields = ['question__titulo',]
    
    def user_num(self, obj):
        users = []
        for user in obj.from_users.all():
            users.append(user)
        return len(users)
    
    class Meta:
        model = Comment_Report

admin.site.register(Comment_Report, Comment_ReportAdmin)



class Profile_ReportAdmin(admin.ModelAdmin):
    readonly_fields = ['timestamp', 'updated', 'classe']
    list_display = ['profile', 'user_num', 'status', 'kind']
    list_filter = ['status', 'kind']
    search_fields = ['question__titulo',]
    
    def user_num(self, obj):
        users = []
        for user in obj.from_users.all():
            users.append(user)
        return len(users)
    
    class Meta:
        model = Profile_Report

admin.site.register(Profile_Report, Profile_ReportAdmin)
