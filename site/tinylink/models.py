from django.db import models
from django.contrib.auth.models import User

# class Users

class Link(models.Model):
    original = models.CharField(max_length=200)
    tiny = models.CharField(max_length=30)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    created = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return '{} by {} on {}'.format(self.tiny, self.user.username, self.created.strftime("%A, %d. %B %Y %I:%M%p"))

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'