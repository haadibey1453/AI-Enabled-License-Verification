from django.db import models

class Unverifiedlog(models.Model):
    ullogid = models.AutoField(db_column='ulLogID', primary_key=True)  # Field name made lowercase.
    noofviolations = models.IntegerField(db_column='NoOfViolations')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'unverifiedlog'
        app_label = 'FYP'