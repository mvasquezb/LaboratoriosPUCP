from django.db import models

# Create your models here.

class Essay(models.Model):
    title_text = models.CharField(max_length=200);
    detail_text = models.CharField(max_length=200)

    def __str__(self):
        return self.title_text

class Test(models.Model):
    essay = models.ManyToManyField(Essay)
    title_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    #1..M with Parameters
    def __str__(self):
        return self.title_text

class LbTestParameter(models.Model):
    #PK
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    #END PK
    title_text = models.CharField(max_length=200)
    detail_text = models.CharField(max_length=200)
    unit_text = models.CharField(max_length=50)

    def __str__(self):
        return self.parameter_title

