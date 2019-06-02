from django.shortcuts import render
from django.conf import settings
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.messages import warning
from django.template import RequestContext
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages,auth
from app.forms import RegisterForm, LoginForm, RoomBooking, Reservations
from datetime import datetime
from app.models import UserDetails, RoomBooking, BookingHistory, Rooms
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from passlib.hash import sha256_crypt
import pymysql
from django.template.defaulttags import register
import smtplib
from app.fusioncharts import FusionCharts
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from collections import OrderedDict

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    global connection, cur, no_of_rooms, rex
    return render(request,'app/index.html')

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(request,'app/contact.html')

def about(request):
    """Renders the about page."""
    return render(request,'app/about.html')

def register(request):
    """Renders the register page."""
    try:
        assert isinstance(request, HttpRequest)
        if request.method=='POST':
            form = RegisterForm(request.POST)
            if(form.is_valid()):
                firstname = form['firstname'].value()
                lastname = form['lastname'].value()
                email = form['email'].value()
                address = form['address'].value()
                password = sha256_crypt.encrypt(form['password'].value())
                user_auth = User.objects.create_user(username=email,first_name=firstname,last_name=lastname,email=email,password=password)
                user = UserDetails(email,address,password)
                user_auth.save()
                user.save()
                return render(request,'app/login.html')
        else:
            form = RegisterForm()
        return render(request,'app/register.html',{'form':form})
    except:
        return render(request,'app/index.html')

def login(request):
    """Renders the login page"""
    try:
        global rex
        assert isinstance(request, HttpRequest)
        if 'email' in request.session:
            return HttpResponseRedirect('/booking')
        if request.method=='POST':
            form = LoginForm(request.POST)
            if(form.is_valid()):
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                login_cred=UserDetails.objects.filter(email=email).values()
                det=User.objects.filter(email=email).values()
                dets=[]
                for i in det:
                    for k,v in i.items():
                        dets.append(v)
                details = login_cred[0]
                superuser = dets[3]
                if email==details['email'] and sha256_crypt.verify(password,details['password']):
                    if 'email' not in request.session:
                        request.session['email']=email
                        request.session['hotel']='Hotel Ruby'
                        if superuser:
                            request.session['admin'] = True
                        else:
                            request.session['admin'] = False
                    rex = booking_hist(request,email)
                    return render(request,'app/booking.html',{'superuser':superuser})
                else:
                    messages.warning(request,'Invalid email/password, Please try again!',extra_tags='alert')
                    return render(request,'app/login.html')
        else:
            form = LoginForm()
            return render(request,'app/login.html')
    except:
        messages.warning(request,'Invalid email/password, Please try again!')
        return render(request,'app/login.html')

def logout(request):
    try:
        users = User.objects.get(email=request.session['email'])
        users.is_active=False
        users.save()
        del(request.session['email'])
        del(request.session['admin'])
        return HttpResponseRedirect('/')
    except:
        return HttpResponseRedirect('/login')

def booking(request):
    """Renders the booking page only after the user logs in"""
    try:
        global available_rooms
        if 'email' in request.session:
            return render(request,'app/booking.html')
        else:
            return HttpResponseRedirect('/login')
    except:
        return HttpResponseRedirect('/login')


def roombooking(request):
    try:
        global room_details, cin, cout, rem
        monthDays={'01':31,'02':28,'03':31,'04':30,'05':31,'06':30,'07':31,'08':31,'09':30,'10':31,'11':30,'12':31} 
        leapDays={'01':31,'02':29,'03':31,'04':30,'05':31,'06':30,'07':31,'08':31,'09':30,'10':31,'11':30,'12':31}         
        room_details = []
        if 'email' in request.session:
            if request.method=='POST':
                form = RoomBooking(request.POST)
                check_in = request.POST.get('checkin')
                cin = changeDateFormat(check_in)
                check_out = request.POST.get('checkout')
                cout = changeDateFormat(check_out)
                dt1 = check_in.split('/')
                dt2 = check_out.split('/')
                diff=int(dt2[1])-int(dt1[1])
                year = int(dt1[2])
                if(year%4==0 and year%100!=0 or year%400==0):
                    days_comp = leapDays[dt1[0]]
                else:
                    days_comp = monthDays[dt1[0]]
                rem = days_comp
                if diff<0:
                    rem = days_comp+diff
                email = request.session['email']
                hotel_name = request.session['hotel']
                room_details = [cin,cout,email,hotel_name]
                return render(request,'app/rooms.html')
        else:
            return render(request,'app/booking.html')
    except:
        return render(request,'app/index.html')

def single(request):
    try:
        if 'email' in request.session:
            if request.method=='POST':
                form = Reservations(request.POST)
                details = get_form(request,form)
                name = details[0]+" "+details[1]+" "+details[2]
                price = rem*1000
                price = price*details[10]
                reservation('single',details,price)
                avl=get_rooms('single')
                avl = len(avl)
                rooms_details = Rooms.objects.filter(roomtype='single').values()
                det=[]
                for i in rooms_details:
                    for k,v in i.items():
                        det.append(v)
                rs = det[2]-details[10]
                if(rs<0):
                    rs = 0
                Rooms.objects.filter(roomtype='single').update(available = rs)
                return render(request,'app/reservation.html',{'name':name,'room':avl,'cin':cin,'cout':cout,'bid':today_date,'price':price,'roomtype':'Single'})
            else:
                avl=get_rooms('single')
                if len(avl)!=0:
                    return render(request,'app/singlerooms.html',{'avl':avl})
                else:
                    messages.warning(request,'No rooms are available')
                    return render(request,'app/singlerooms.html',{'avl':avl})
        else:
            return render(request,'app/login.html')
    except:
        return render(request,'app/booking.html')

def double(request):
    try:
        if 'email' in request.session:
            if request.method=='POST':
                form = Reservations(request.POST)
                details = get_form(form)
                name = details[0]+" "+details[1]+" "+details[2]
                price = rem*1500
                price = price*no_of_rooms
                reservation('double',details,price)
                avl=get_rooms('double')
                avl = len(avl)
                rooms_details = Rooms.objects.filter(roomtype='double').values()
                det=[]
                for i in rooms_details:
                    for k,v in i.items():
                        det.append(v)
                rs = det[2]-details[10]
                if(rs<0):
                    rs = 0
                Rooms.objects.filter(roomtype='double').update(available = rs)
                return render(request,'app/reservation.html',{'name':name,'room':rooms,'cin':cin,'cout':cout,'bid':today_date,'price':price,'roomtype':'Double','avl':available})
            else:
                avl=get_rooms('double')
                if len(avl)!=0:
                    return render(request,'app/doublerooms.html',{'avl':avl})
                else:
                    messages.warning(request,'No rooms are available')
                    return render(request,'app/doublerooms.html',{'avl':avl})
        else:
            return render(request,'app/login.html')
    except:
        return render(request,'app/booking.html')

def deluxe(request):
    try:
        if 'email' in request.session:
            if request.method=='POST':
                form = Reservations(request.POST)
                details = get_form(form)
                name = details[0]+" "+details[1]+" "+details[2]
                price = rem*3500
                price = price*request.session['rooms']
                reservation('deluxe',details,price)
                avl=get_rooms('deluxe')
                avl = len(avl)
                rooms_details = Rooms.objects.filter(roomtype='deluxe').values()
                det=[]
                for i in rooms_details:
                    for k,v in i.items():
                        det.append(v)
                rs = det[2]-details[10]
                if(rs<0):
                    rs = 0
                Rooms.objects.filter(roomtype='deluxe').update(available = rs)
                return render(request,'app/reservation.html',{'name':name,'room':rooms,'cin':cin,'cout':cout,'bid':today_date,'price':price,'roomtype':'Deluxe'})
            else:
                avl=get_rooms('deluxe')
                if len(avl)!=0:
                    return render(request,'app/deluxe.html',{'avl':avl})
                else:
                    messages.warning(request,'No rooms are available')
                    return render(request,'app/deluxe.html',{'avl':avl})
        else:
            return render(request,'app/login.html')
    except:
        return render(request,'app/booking.html')

def luxury(request):
    try:
        if 'email' in request.session:
            if request.method=='POST':
                form = Reservations(request.POST)
                details = get_form(form)
                name = details[0]+" "+details[1]+" "+details[2]
                price = rem*5000
                price = price*no_of_rooms
                reservation('luxury',details,price)
                avl=get_rooms('luxury')
                avl = len(avl)
                rooms_details = Rooms.objects.filter(roomtype='luxury').values()
                det=[]
                for i in rooms_details:
                    for k,v in i.items():
                        det.append(v)
                rs = det[2]-details[10]
                if(rs<0):
                    rs = 0
                Rooms.objects.filter(roomtype='luxury').update(available = rs)
                return render(request,'app/reservation.html',{'name':name,'room':rooms,'cin':cin,'cout':cout,'bid':today_date,'price':price,'roomtype':'Deluxe'})
            else:
                avl=get_rooms('luxury')
                if len(avl)!=0:
                    return render(request,'app/luxury.html',{'avl':avl})
                else:
                    messages.warning(request,'No rooms are available')
                    return render(request,'app/luxury.html',{'avl':avl})
        else:
            return render(request,'app/login.html')
    except:
        return render(request,'app/booking.html')

def executive(request):
    try:
        if 'email' in request.session:
            if request.method=='POST':
                form = Reservations(request.POST)
                details = get_form(form)
                name = details[0]+" "+details[1]+" "+details[2]
                price = rem*6500
                price = price*request.session['rooms']
                reservation('executive',details,price)
                avl=get_rooms('executive')
                avl = len(avl)
                rooms_details = Rooms.objects.filter(roomtype='executive').values()
                det=[]
                for i in rooms_details:
                    for k,v in i.items():
                        det.append(v)
                rs = det[2]-details[10]
                if(rs<0):
                    rs = 0
                Rooms.objects.filter(roomtype='executive').update(available = rs)
                return render(request,'app/reservation.html',{'name':name,'room':rooms,'cin':cin,'cout':cout,'bid':today_date,'price':price,'roomtype':'Deluxe'})
            else:
                avl=get_rooms('executive')
                if len(avl)!=0:
                    return render(request,'app/executive.html',{'avl':avl})
                else:
                    messages.warning(request,'No rooms are available')
                    return render(request,'app/executive.html',{'avl':avl})
        else:
            return render(request,'app/login.html')
    except:
        return render(request,'app/booking.html')

def presidential(request):
    try:
        if 'email' in request.session:
            if request.method=='POST':                
                form = Reservations(request.POST)
                details = get_form(form)
                name = details[0]+" "+details[1]+" "+details[2]
                price = rem*8000
                price = price*request.session['rooms']
                reservation('presidential',details,price)
                avl=get_rooms('presidential')
                avl = len(avl)
                rooms_details = Rooms.objects.filter(roomtype='presidential').values()
                det=[]
                for i in rooms_details:
                    for k,v in i.items():
                        det.append(v)
                rs = det[2]-details[10]
                if(rs<0):
                    rs = 0
                Rooms.objects.filter(roomtype='presidential').update(available = rs)
                return render(request,'app/reservation.html',{'name':name,'room':rooms,'cin':cin,'cout':cout,'bid':today_date,'price':price,'roomtype':'Deluxe'})
            else:
                avl=get_rooms('presidential')
                if len(avl)!=0:
                    return render(request,'app/presidential.html',{'avl':avl})
                else:
                    messages.warning(request,'No rooms are available')
                    return render(request,'app/presidential.html',{'avl':avl})
        else:
            return render(request,'app/login.html')
    except:
        return render(request,'app/booking.html')

def reservation(room,details,price):
        try:
            global today_date
            today_date = int(datetime.now().strftime("%Y%m%d%H%M%S"))
            rb = RoomBooking(today_date,room_details[0],room_details[1],details[0],details[1],details[2],details[3],details[4],details[5],details[6],details[7],details[8],details[9],details[10])
            rb.save()
            user = User.objects.get(email=room_details[2])
            arguments = [today_date,room_details[0],room_details[1],user.email,user.id,price]
            bh = BookingHistory(arguments[0],arguments[1],arguments[2],arguments[3],arguments[4])
            bh.save()
        except:
            return HttpResponseRedirect('/booking')


def update_rooms(roomtype,available,no_of_rooms):
    try:
        rooms_details = Rooms.objects.filter(roomtype=roomtype).values()
        det=[]
        for i in rooms_details:
            for k,v in i.items():
                det.append(v)
        rs = det[2]-det[3]
        if(rs<0):
            rs = 0
        room_details.available = rs
        room_details.save()
    except:
        return render(request,'app/booking.html')

def changeDateFormat(date):
    d_list = date.split('/')
    modified_date = d_list[2]+'-'+d_list[0]+'-'+d_list[1]
    return modified_date

def bookinghistory(request):
    try:
        red = booking_hist(request,request.session['email'])
        return render(request,'app/booking_history.html',{'details':red})
    except:
        return render(request,'app/booking.html')

def booking_hist(request,email):
    try:
        bhr = BookingHistory.objects.filter(email=email).values()
        det=[]
        details = []
        for i in bhr:
            det=[]
            for k,v in i.items():
                det.append(v)
            details.append(det)
        return details
    except:
        return render(request,'app/booking.html')

def forgotpassword(request):
    try:
        if request.method=='POST':
            fromaddr = 'ruby.coders@gmail.com'
            toaddrs  = request.POST.get('email')
            data = UserDetails.objects.filter(email=toaddrs).values()
            msg = 'Hello, your password is P@$sword '
            username = 'ruby.coders@gmail.com'
            password = '$uperSt@r007'
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(username,password)
            server.sendmail(fromaddr, toaddrs, msg)
            server.quit()
            return redirect(url_for('login'))
        else:
            return render(request,'app/forgotpassword.html')
    except:
        messages.warning(request,'Invalid email please enter valid email')
        return render(request,'app/forgotpassword.html')

def rooms(request):
    assert isinstance(request, HttpRequest)
    return render(request,'app/display_rooms.html')

def adminlogin(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        login_cred=UserDetails.objects.filter(email=email).values()
        det=User.objects.filter(email=email).values() 
        details = login_cred[0]
        if email==details['email'] and sha256_crypt.verify(password,details['password']):
            request.session['email']=email
            request.session['hotel']='Hotel Ruby' 
            return HttpResponseRedirect('/adminruby')
        else:
            messages.warning(request,'Not an admin, please contact administrator')
            return render(request,'app/adminlogin.html')
    else:
        return render(request,'app/adminlogin.html')      


def adminruby(request):
    dataSource = OrderedDict()

    # The `chartConfig` dict contains key-value pairs data for chart attribute
    chartConfig = OrderedDict()
    chartConfig["caption"] = ""
    #chartConfig["subCaption"] = "In MMbbl = One Million barrels"
    chartConfig["xAxisName"] = "Rooms"
    chartConfig["yAxisName"] = "Available"
    chartConfig["numberSuffix"] = ""
    chartConfig["theme"] = "fusion"

    # The `chartData` dict contains key-value pairs data
    chartData = OrderedDict()
    avl1 = get_rooms('single')
    avl1 = len(avl1)
    avl2 = get_rooms('double')
    avl2 = len(avl2)
    avl3 = get_rooms('luxury')
    avl3 = len(avl3)
    avl4 = get_rooms('deluxe')
    avl4 = len(avl4)
    avl5 = get_rooms('executive')
    avl5 = len(avl5)
    avl6 = get_rooms('presidential')
    avl6 = len(avl6)

    chartData["Single"] = avl1
    chartData["Double"] = avl2
    chartData["Deluxe"] = avl3
    chartData["Luxury"] = avl4
    chartData["Executive"] = avl5
    chartData["Presidential"] = avl6

    dataSource["chart"] = chartConfig
    dataSource["data"] = []
    
    # Convert the data in the `chartData` array into a format that can be consumed by FusionCharts. 
    # The data for the chart should be in an array wherein each element of the array is a JSON object
    # having the `label` and `value` as keys.

    # Iterate through the data in `chartData` and insert in to the `dataSource['data']` list.
    for key, value in chartData.items():
        data = {}
        data["label"] = key
        data["value"] = value
        dataSource["data"].append(data)


    # Create an object for the column 2D chart using the FusionCharts class constructor
    # The chart data is passed to the `dataSource` parameter.
    column2D = FusionCharts("column2d", "ex1" , "800", "400", "chart-1", "json", dataSource)

    return  render(request, 'app/adminanalytics.html', {'output' : column2D.render(), 'chartTitle': 'Available Rooms'})

def getusers(request):
    usr = User.objects.all()
    users=[]
    list2=[]
    for i in usr:
        users.append(i)
    for u in users:
        dets = User.objects.filter(email = u).values()
        list1 =[]
        for k in dets:
            list1.append(k['id'])
            list1.append(k['first_name'])
            list1.append(k['last_name'])
            list1.append(k['email'])
            list1.append(k['date_joined'])
        list2.append(list1)
    return render(request,'app/getusers.html',{'list':list2})

def adminbooking(request):
    try:
        bhr = BookingHistory.objects.all()
        paginator = Paginator(bhr, 10)
        page = request.GET.get('page', 1)
        try:
            bookings = paginator.page(page)
            return render(request,'app/adminbooking.html',{'bookings':bookings})
        except PageNotAnInteger:
            bookings = paginator.page(1)
        except EmptyPage:
            bookings = paginator.page(paginator.num_pages)    
            return render(request,'app/adminbooking.html')
    except:
        return render(request,'app/adminruby.html')

def get_form(request,form):
    firstname = form['firstname'].value()
    middlename = form['middlename'].value()
    lastname = form['lastname'].value()
    email = form['email'].value()
    phone = form['phone'].value()
    address = form['address'].value()
    city = form['city'].value()
    state = form['state'].value()
    zipcode = form['zipcode'].value()
    idproof = form['idproof'].value()
    rooms = form['rooms'].value()
    no_of_rooms = int(rooms)
    list = [firstname,middlename,lastname,email,phone,address,city,state,zipcode,idproof,no_of_rooms]
    return list

def get_rooms(roomtype):
    available = Rooms.objects.filter(roomtype=roomtype).values()
    det=[]
    for i in available:
        for k,v in i.items():
            det.append(v)
    avl = det[3]
    available_rooms = avl
    avail= []
    for i in range(1,avl+1):
        avail.append(i)
    return avail