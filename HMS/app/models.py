from django.db import models

class UserDetails(models.Model):
    email = models.EmailField(max_length=100,primary_key=True)
    address = models.TextField(max_length=400)
    password = models.CharField(max_length=140, default='NULL')

    class Meta:
        db_table = 'user'

    def __str__(self):
        return u'%s %s'  % (self.email,self.address)

STATES = (
        ('Alabama','AL'),('Alaska','AK'),('Arizona','AZ'),('Arkansas','AR'),('California','CA'),
        ('Colorado','CO'),('Connecticut','CT'),('Delaware','DE'),('Florida','FL'),('Georgia','GA'),
        ('Hawaii','HI'),('Idaho','ID'),('Illinois','IL'),('Indiana','IN'),('Iowa','IA'),
        ('Kansas','KS'),('Kentucky','KY'),('Louisiana','LA'),('Maine','ME'),('Maryland','MD'),
        ('Massachusetts','MA'),('Michigan','MI'),('Minnesota','MN'),('Mississippi','MS'),('Missouri','MO'),
        ('Montana','MT'),('Nebraska','NE'),('Nevada','NV'),('New Hampshire','NH'),('New Jersey','NJ'),
        ('New Mexico','NM'),('New York','NY'),('North Carolina','NC'),('North Dakota','ND'),('Ohio','OH'),
        ('Oklahoma','OK'),('Oregon','OR'),('Pennsylvania','PA'),('Rhode Island','RI'),('South Carolina','SC'),
        ('South Dakota','SD'),('Tennessee','TN'),('Texas','TX'),('Utah','UT'),('Vermont','VT'),
        ('Virginia','VA'),('Washington','WA'),('West Virginia','WV'),('Wisconsin','WI'),('Wyoming','WY'),
    )

class HotelRegister(models.Model):
    hotel_id = models.AutoField(primary_key=True)
    hotel_name = models.CharField(max_length=250,unique=True,blank=False)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length = 20,choices = STATES,default='Alabama')
    zip = models.CharField(max_length = 20)
    email = models.EmailField(max_length = 100)
    password = models.CharField(max_length = 50)
    contact = models.IntegerField()

    class Meta:
        db_table ='hotels'

class HotelBooking(models.Model):
    hotelid = models.ForeignKey(HotelRegister,on_delete=models.CASCADE)
    roomtype = models.CharField(max_length = 50)
    count = models.IntegerField()
    availability = models.IntegerField()

    class Meta:
        db_table ='hotelbooking'


class RoomBooking(models.Model):
    ROOM_CHOICES = (
    ('deluxe','DELUXE'),
    ('luxury', 'LUXURY'),
    )
    checkin  = models.DateField(blank=True)
    checkout = models.DateField(blank=True)
    email = models.CharField(max_length=100)
    hotel_name = models.CharField(max_length = 10)
    room = models.CharField(max_length=10, choices=ROOM_CHOICES, default='deluxe')

    class Meta:
        db_table = 'roombooking'

class BookingInformation(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.IntegerField()
    address = models.CharField(max_length=150)
    requirements = models.CharField(max_length=100,blank=True)
    booking_id = models.CharField(max_length=100,primary_key=True)

    class Meta:
        db_table = 'bookinginfo'