from django.db import models
from django.contrib.auth.models import User
from .conf import TestStatus


class TestCase(models.Model):
    name = models.CharField(default='',
                            null=False,
                            max_length=100,
                            unique=True)
    description = models.CharField(default='',
                                   null=False,
                                   blank=True,
                                   max_length=1000)
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               related_name='tests',
                               null=True)

    @property
    def status(self):
        # due to runs order by -id
        test_run = self.runs.first()
        if test_run is None:
            return TestStatus.NORUN
        else:
            return test_run.status


class TestRun(models.Model):
    class Meta:
        ordering = ['-timestamp']
        get_latest_by = 'timestamp'

    test_case = models.ForeignKey(TestCase,
                                  on_delete=models.CASCADE,
                                  related_name='runs')
    status = models.CharField(choices=TestStatus.choices(),
                              max_length=10)
    executor = models.ForeignKey(User,
                                 on_delete=models.SET_NULL,
                                 related_name='runs',
                                 null=True,
                                 blank=True)
    timestamp = models.DateTimeField(auto_now=True)