from django.db import models


class Topic(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    is_show = models.BooleanField(default=True)

    class Meta:
        db_table = 'Topic'


class Subtopic(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    is_show = models.BooleanField(default=True)
    topic = models.OneToOneField(Topic, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'Subtopic'


class ModelClass(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    is_show = models.BooleanField(default=True)
    sub_topic = models.OneToOneField(Subtopic, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'Model_Class'


class ModelDetails(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    is_show = models.BooleanField(default=True)
    model_class = models.OneToOneField(ModelClass, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'Model_Details'
