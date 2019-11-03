from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    profile_picture = models.ImageField(upload_to='user/%Y/%m/%d', blank=True, default='person.png')
    date_of_birth = models.DateField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("account_detail", kwargs={'pk': self.user.pk, 'username': self.user.username})
    

    def __str__(self):
        return '{0}\'s profile'.format(self.user.username)


class Contact(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_from', on_delete=models.CASCADE)
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_to', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)


User.add_to_class('following', models.ManyToManyField('self', through=Contact, related_name='followers', symmetrical=False))

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save_account(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
