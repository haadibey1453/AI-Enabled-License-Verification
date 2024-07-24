from django.db import models

class Login(models.Model):
    login_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'login'
        app_label = 'FYP'
