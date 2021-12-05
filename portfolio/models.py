from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    pass

@receiver(post_save, sender=CustomUser)
def create_profile(sender, **kwargs):
    """ 新ユーザー作成時に空のprofileも作成する """
    if kwargs['created']:
        profile = Profile.objects.get_or_create(user=kwargs['instance'])

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), verbose_name='ユーザー', on_delete=models.CASCADE, default='')
    name = models.CharField(max_length=50, blank=True, null=True, default='Anonymous', verbose_name='氏名')
    come_from = models.CharField(max_length=50, blank=True, null=True, default='', verbose_name='出身')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='生年月日')
    hobby = models.CharField(max_length=100, blank=True, null=True, default='', verbose_name='趣味')
    career = models.TextField(default='', blank=True, verbose_name='経歴')
    contact = models.URLField(default='', blank=True, null=True, verbose_name='GitHubページ')

    def __str__(self):
        if self.name != '':
            return f'# {self.id}: {self.name}'
        else:
            return f'# {self.id}: {self.user.username}'


class Skill(models.Model):
    SKILL_CATEGORY = (
        (0, None),
        (1, '言語'),
        (2, 'フレームワーク'),
        (3, 'データベース、サーバー等')
    )
    name = models.CharField(max_length=50, verbose_name='スキル名')
    category = models.IntegerField(choices=SKILL_CATEGORY, default=0, null=True, blank=True, verbose_name='スキル種別')

    def __str__(self):
        return self.name 

class Service(models.Model):
    developer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, verbose_name='開発者')
    name = models.CharField(max_length=50, verbose_name='サービス名')
    outline = models.TextField(default='', blank=True, verbose_name='概要')
    description = models.TextField(default='', blank=True, verbose_name='内容')
    skills = models.ManyToManyField(Skill, verbose_name='使用言語等', related_name='skill_detail')
    service_url = models.URLField(blank=True, null=True, verbose_name='サービスURL')
    code_url = models.URLField(blank=True, null=True, verbose_name='ソースコード')

    def __str__(self):
        return self.name
