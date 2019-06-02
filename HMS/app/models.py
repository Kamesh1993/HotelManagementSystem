from django.db import models
from django.contrib.auth.models import User

class UserDetails(models.Model):
    email = models.EmailField(max_length=100,primary_key=True)
    address = models.TextField(max_length=400)
    password = models.CharField(max_length=140, default='NULL')

    class Meta:
        db_table = 'user'

    def __str__(self):
        return u'%s %s'  % (self.email,self.address)

class RoomBooking(models.Model):
    bookingid = models.BigIntegerField(primary_key=True,default=0)
    checkin  = models.CharField(max_length=140,default='NULL')
    checkout = models.CharField(max_length=140,default='NULL') 
    firstname = models.CharField(max_length=140)
    middlename = models.CharField(max_length=140)
    lastname = models.CharField(max_length=140)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10)
    address = models.TextField(max_length=400)
    city = models.CharField(max_length=140)
    state = models.CharField(max_length=140)
    zipcode = models.IntegerField()
    idproof = models.CharField(max_length=140)
    rooms = models.CharField(max_length=40)
    
    class Meta:
        db_table = 'roombooking'

    def __str__(self):
        return u'%s %s %s %s %s %s %s %s %s %s %s %s %s %s' %(self.bookingid,
        self.checkin,self.checkout,self.firstname,self.middlename,
        self.lastname,self.email,self.phone,self.address,self.city,
        self.state,self.zipcode,self.idproof,self.rooms)

class BookingHistory(models.Model):
    bookingid = models.BigIntegerField(primary_key=True,default=0)
    checkin  = models.CharField(max_length=140,default='NULL')
    checkout = models.CharField(max_length=140,default='NULL')
    email = models.EmailField(max_length=50)
    userid = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'bookinghistory'

    def __str__(self):
        return u'%s %s %s %s %s' %(self.bookingid,self.checkin,self.checkout,self.email,self.userid)

class Rooms(models.Model):
    roomtype  = models.CharField(max_length=140,default='NULL')
    total = models.BigIntegerField(default=0)
    available = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'rooms'

    def __str__(self):
        return u'%s %s %s' %(self.roomtype,self.total,self.available)

