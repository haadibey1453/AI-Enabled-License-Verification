from django.db import models

class DriverLicenseInfo(models.Model):
    license_no = models.CharField(primary_key=True, max_length=9)
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=50)  # Field name made lowercase.
    height = models.FloatField(db_column='Height')  # Field name made lowercase.
    cnic = models.CharField(db_column='CNIC', max_length=15)  # Field name made lowercase.
    date_of_birth = models.DateField(db_column='Date_Of_Birth')  # Field name made lowercase.
    blood_group = models.CharField(db_column='Blood_Group', max_length=3)  # Field name made lowercase.
    issue_date = models.DateField(db_column='Issue_Date')  # Field name made lowercase.
    expiry_date = models.DateField(db_column='Expiry_Date')  # Field name made lowercase.
    image = models.CharField(db_column='Image', max_length=100)  # Field name made lowercase.
    face_embedding = models.CharField(db_column='Face_Embedding', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'driver_license_info'
        app_label = 'FYP'
