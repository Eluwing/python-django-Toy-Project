from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import datetime # Used to get the current date

# Create your models here.
class Post(models.Model):
    p_title = models.CharField('Posted Title',max_length = 30, help_text = 'You can enter up to 30 characters.')
    p_name = models.CharField('Posted name',max_length = 10, help_text = 'You can enter up to 10 characters.')
    p_date = models.DateField('Posted date',default = datetime.date.today)
    p_description = models.TextField('Text',max_length = 500)

    class Meta:
        ordering = ['p_date']

    def __str__(self):
        return self.p_title

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])

class Comment(models.Model):
    c_name = models.CharField('Commented name',max_length = 10, help_text = 'You can enter up to 10 characters.')
    c_date = models.DateField('Commented date',default = datetime.date.today)
    c_description = models.CharField('Text',max_length = 100, help_text = 'Enter your comment. n\You can enter up to 100 characters.')
    post = models.ForeignKey('post', on_delete = models.SET_NULL, null = True)

    class Meta:
        ordering = ['c_date']

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.post.id)])

    def __str__(self):
        return self.c_description
