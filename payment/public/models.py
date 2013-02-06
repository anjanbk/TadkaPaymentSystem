from django.db import models

# Represents a singing gram time-slot
class Timeslot(models.Model):
	id = models.AutoField(primary_key=True)
	
	# 0 = Monday, 1 = Tuesday, 2 = Wednesday, 3 = Thursday, 4 = Friday
	day = models.IntegerField()
	time = models.CharField(max_length=5)
	availability = models.BooleanField()
	def __unicode__(self):
		return "Day: " + str(self.day) + ", Time: " + self.time;
