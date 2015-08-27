from django.contrib import admin

from .models import NotiAnswer, NotiVote, NotiFollow, NotiComment
# Register your models here.





class NotiAnswerAdmin(admin.ModelAdmin):
    readonly_fields = ['timestamp', 'updated', 'kind']
    list_display = ['to_user', 'from_user', 'unread', 'question']
    list_filter = ['unread']
    search_fields = ['question__titulo', 'to_user__username', 'to_user__email']
    
    class Meta:
        model = NotiAnswer

admin.site.register(NotiAnswer, NotiAnswerAdmin)


class NotiVoteAdmin(admin.ModelAdmin):
    readonly_fields = ['timestamp', 'updated', 'kind']
    list_display = ['to_user', 'from_user', 'unread', 'vote', 'question', 'answer']
    list_filter = ['unread']
    search_fields = ['question__titulo', 'answer__resposta', 'to_user__username', 'to_user__email']
    
    class Meta:
        model = NotiVote

admin.site.register(NotiVote, NotiVoteAdmin)


class NotiFollowAdmin(admin.ModelAdmin):
    readonly_fields = ['timestamp', 'updated', 'kind']
    list_display = ['to_user', 'from_user', 'unread']
    list_filter = ['unread']
    search_fields = ['to_user__username', 'to_user__email', 'from_user__username', 'from_user__email']
    
    class Meta:
        model = NotiFollow

admin.site.register(NotiFollow, NotiFollowAdmin)



class NotiCommentAdmin(admin.ModelAdmin):
    readonly_fields = ['timestamp', 'updated', 'kind']
    list_display = ['to_user', 'from_user', 'unread']
    list_filter = ['unread']
    search_fields = ['to_user__username', 'to_user__email', 'from_user__username', 'from_user__email']
    
    class Meta:
        model = NotiComment

admin.site.register(NotiComment, NotiCommentAdmin)
