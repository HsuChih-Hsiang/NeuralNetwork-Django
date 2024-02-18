from django.db import models
from utility.models import BaseModel


class Member(BaseModel):
    member_id = models.AutoField(primary_key=True)
    account = models.CharField(max_length=20, unique=True)
    password = models.CharField()
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'Member'


class MemberPermission(BaseModel):
    member_id = models.OneToOneField(Member, on_delete=models.CASCADE)
    read_only = models.BooleanField()
    admin = models.BooleanField()

    class Meta:
        db_table = 'Member_Permission'
