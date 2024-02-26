from django.db import models


class Member(models.Model):
    objects = models.Manager()
    member_id = models.AutoField(primary_key=True)
    account = models.CharField(max_length=20, unique=True)
    password = models.CharField()
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'Member'


class MemberPermission(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    read_only = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)

    class Meta:
        db_table = 'Member_Permission'
