from django.db import models
from django.conf import settings
# Create your models here.


class Schemas(models.Model):
    title = models.CharField(max_length=50)
    Column_separator = models.CharField(max_length=50, default="Comma (,)")
    String_character = models.CharField(max_length=50, default='Double-quote (")')
    Post_date = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fields = models.TextField(default="[()]")
    # Fields syntax (<name of field>, <type of field>, <from>, <to>, <sentences>)
    # from/to/sentences can be None


class CsvFile(models.Model):
    filename = models.CharField(max_length=50)  # example 5_20.csv\10_100.csv
    create_date = models.DateField()
    schema_id = models.IntegerField()
    is_ready = models.BooleanField()
