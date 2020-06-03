# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class CustomManager(models.Manager):	# (custom entries)
	def get_queryset(self):
		return super(CustomManager, self).get_queryset().filter(region='UK')


class Azureratecardtable(models.Model):
    region = models.CharField(max_length=20)
    ratecard = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
       	db_table = 'azureratecardtable'

    #objects = models.Manager()			# Instantiating the dafault Manager (custom entry)
    #cm = CustomManager()				# Instantiating my custom manager class.  (custom entry)


