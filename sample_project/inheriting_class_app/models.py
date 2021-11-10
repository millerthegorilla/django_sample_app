from django.db import models, DEFAULT_DB_ALIAS
from django.contrib.auth.models import User
from django.conf import settings

from base_app.models import Comment, Post


class ForumPost(Post):
    author: models.CharField = models.CharField(default='', max_length=40)
    active: models.BooleanField = models.BooleanField(default=True)
    moderation: models.DateField = models.DateField(null=True, default=None, blank=True)
    pinned:models.SmallIntegerField = models.SmallIntegerField(default=0)
    subscribed_users: models.ManyToManyField = models.ManyToManyField(
        User, blank=True, related_name="subscribed_posts")

    class Meta:
        ordering = ['-date_created']
        permissions = [('approve_post', 'Approve Post')]

    category: models.CharField = models.CharField(
        max_length=2,
        choices=settings.CATEGORY.choices,
        default=settings.CATEGORY.GENERAL,
    )

    location: models.CharField = models.CharField(
        max_length=2,
        choices=settings.LOCATION.choices,
        default=settings.LOCATION.ANY_ISLE,
    )

    def get_absolute_url(self) -> str:
        return reverse_lazy(
            'django_forum_app:post_view', args=(
                self.id, self.slug,)) # type: ignore

    # def __str__(self) -> str:
    #     return f"Post by {self.author}"

    def category_label(self) -> str:
        return settings.CATEGORY(self.category).label

    def location_label(self) -> str:
        return settings.LOCATION(self.location).label


class ForumComment(Comment):
    forum_post: models.ForeignKey = models.ForeignKey(
        ForumPost, on_delete=models.CASCADE, related_name="forum_comments")
    active: models.BooleanField = models.BooleanField(default='True')
    moderation: models.DateField = models.DateField(null=True, default=None, blank=True)
    title_slug: models.SlugField = models.SlugField()

    class Meta:
        ordering = ['date_created']
        permissions = [('approve_comment', 'Approve Comment')]

    def save(self, force_insert=False, force_update=False, using=DEFAULT_DB_ALIAS, update_fields=None) -> None:
        self.post = self.forum_post
        super().save()

    def get_absolute_url(self) -> str:
        return self.forum_post.get_absolute_url() + '#' + self.title

    def get_category_display(self) -> str:
        return 'Comment'