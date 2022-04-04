import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    
    def __str__(self):
        return self.question_text
    
    #needs placed right above function:
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    
    #second ed:
    def was_published_recently(self):
        nowTime = timezone.now()
        
        #ret true if pub_date is less than rn + larger than a day ago's date
        return (nowTime - datetime.timedelta(days=1)) <= self.pub_date <= nowTime
    
    """First ed: (future date bug)
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    """
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
