from django.db import models
from django.contrib.auth.models import User
from .conf import TestStatus
from dbview.models import DbView


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


class TestCaseStat(DbView):
    class Meta:
        ordering = ['-test_case']

    test_case = models.OneToOneField(TestCase, primary_key=True, db_column='test_id', on_delete=models.DO_NOTHING)
    status = models.CharField(choices=TestStatus.choices(),
                              max_length=10)
    last_executor = models.ForeignKey(User,
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      blank=True,
                                      db_column='last_executor')

    @classmethod
    def get_view_str(cls):
        return """
                CREATE VIEW tcm_testcasestat AS (
                Select tc.id as test_id, tr.status as status, tr.executor_id as last_executor
                FROM tcm_testcase tc
                LEFT JOIN (
                    SELECT DISTINCT ON (r.test_case_id) r.*
                        FROM tcm_testrun r
                        ORDER BY r.test_case_id, r.timestamp DESC) tr
                ON tc.id = tr.test_case_id
            )
            """
