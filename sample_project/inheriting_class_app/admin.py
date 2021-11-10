from django.contrib import admin
from base_app.models import Comment
import logging

from django.contrib import admin
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.utils.translation import ngettext
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import ForumPost, ForumComment

logger = logging.getLogger('django_artisan')


# Register your models here.
@admin.register(ForumComment)
class ForumCommentAdmin(admin.ModelAdmin):  # SoftDeletionAdmin):
    #fields = ('moderation', 'active', 'author', 'title', 'text', 'date_created', 'deleted_at', 'user_profile')
    # fieldsets = [
    #     ('Moderation', {'fields': ['moderation']}),
    #     ('Active', {'fields': ['active']}),
    #     ('Author', {'fields': ['author']}),
    #     ('Text', {'fields': ['text']}),
    # ]
    list_display = ('moderation', 'active', 'post_str',
                    'author', 'text', 'date_created') # 'deleted_at')
    list_editable = ('text', )
    list_filter = ('moderation', 'active', 'date_created',
                   'post', 'author') # 'deleted_at')
    search_fields = ('author', 'text')

    def post_str(self, obj: ForumComment) -> str:
        link = reverse("admin:inheriting_class_app_forumpost_change",
                       args=[obj.forum_post.id])
        return mark_safe(
            f'<a href="{link}">{escape(obj.forum_post.__str__())}</a>')

    post_str.short_description = 'ForumPost' # type: ignore
    # make row sortable
    post_str.admin_order_field = 'forumpost'  # type: ignore

    actions = ['approve_comment']

    def approve_comment(self, request: HttpRequest, queryset: QuerySet):
        updated = queryset.update(moderation=None)
        # idx = 0
        # for q in queryset:
        #     q.moderation = None
        #     try:
        #         q.save(update_fields=['moderation'])
        #         idx += 1
        #     except Exception as e:
        #         logger.error("Error approving moderation : {0}".format(e))
        
        self.message_user(request,
                          ngettext(
                                '%d comment was approved.',
                                '%d comments were approved.',
                                updated,
                          ) % updated, 
                          messages.SUCCESS)


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('pinned', 'moderation', 'active', 'author',
                    'title', 'text', 'date_created')
    list_filter = ('pinned', 'moderation', 'active',
                   'date_created', 'author')
    search_fields = ('author', 'text', 'title')

    actions = ['approve_post']

    def approve_post(self, request: HttpRequest, queryset: QuerySet):
        idx = 0
        for q in queryset:
            q.moderation = None
            try:
                q.save(update_fields=['moderation'])
                idx += 1
            except Exception as e:
                logger.error("Error approving moderation : {0}".format(e))
        
        self.message_user(request,
                          ngettext(
                                '%d post was approved.',
                                '%d posts were approved.',
                                idx,
                          ) % idx, 
                          messages.SUCCESS)

    # def pin_post(self, request: HttpRequest queryset):
    #     self.message_user(request: HttpRequest ngettext(
    #                 '%d post was approved.',
    #                 '%d posts were approved.',
    #                 updated,
    #             ) % updated, messages.SUCCESS)
