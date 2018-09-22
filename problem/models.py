from django.db import models
from django.contrib.postgres.fields import JSONField

from account.models import User


class ProblemTag(models.Model):
    name = models.CharField(max_length=127)


class ProblemMixin(object):
    title = models.CharField(max_length=128)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    # ms
    time_limit = models.IntegerField()
    # MB
    memory_limit = models.IntegerField()

    description = models.TextField()
    input_description = models.TextField(blank=True, null=True)
    output_description = models.TextField(blank=True, null=True)

    # key-value field
    samples = JSONField(default={})


class Problem(models.Model):
    oj = models.CharField(max_length=128, default='')
    pid = models.CharField(max_length=64, default='')

    title = models.CharField(max_length=128)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    # ms
    time_limit = models.IntegerField()
    # MB
    memory_limit = models.IntegerField()

    test_cases = models.CharField(max_length=128)
    scores = JSONField(default={})

    @property
    def uid(self):
        return self.pid if self.oj else str(self.id)
