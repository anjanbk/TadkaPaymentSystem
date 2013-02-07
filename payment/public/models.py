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

# Represents a completed and processed purchase order
class Order(models.Model):
	id = models.AutoField(primary_key=True)
	
	# Optional field for the internal client
	tadkaSeller = models.CharField(max_length=50)

	senderName = models.CharField(max_length=50)
	senderGender = models.CharField(max_length = 10)
	senderPhone = models.CharField(max_length=15)
	receiverName = models.CharField(max_length=50)
	receiverGender = models.CharField(max_length = 10)
	timeslot = models.CharField(max_length = 10)
	location = models.CharField(max_length = 100)
	song = models.CharField(max_length = 100)
	def __unicode__(self):
		return "From: " + self.senderName + ", To: " + self.receiverName
