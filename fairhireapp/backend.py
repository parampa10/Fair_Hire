from random import randint
import random
import string
from django.http import JsonResponse
from django.shortcuts import render
# from product_analysis.models import Caps, Decoration, Material, Shape, platforms, user, files, Formats
from fairhireapp.models import Complaints, User, User_Logged
from django.db.models import Q
from django.shortcuts import redirect
import json
from rest_framework.decorators import api_view
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

from django.core.mail import EmailMessage, get_connection

# Thigs we store in sessions = userid, user_logged_in, loggedin_user
# if 'user_logged_in' in request.session:
#             if (request.session['user_logged_in'] == "True"): 
#                 pass
#             else: 
#                 return render(request,"login.html",{ "message" : message })
def userloggedin(request):
    
    if 'userid' in request.session:
            
            if (request.session['userid'] != ""): 
                return {"userid": request.session['userid'], "loggedin_user": request.session['loggedin_user']}
            else: 
                return {"userid":""}
    else:
        return {"userid":""}

def logout(request):
    print(request.session['userid'])
    request.session['userid'] = ""
    request.session['user_logged_in'] = ""
    request.session['loggedin_user']=""
    return render(request,"login.html")
from django.db.models import Count

def login(request):

    # return render(request,"dashboard.html")

    message = ""
    
    if request.method == 'POST':
        
        criterion1 = Q(userid =  request.POST["userid"]) #any query you want
        criterion2 = Q(password=request.POST["password"]) #any query you want
        isalready = User.objects.filter(criterion1 & criterion2 ).values()
        values = list(isalready)
    
        if(len(values)==0):
            message = "This user is not registered"
            # print("Hello")
            return JsonResponse(message, safe=False)
        else:
            message = "login successful"

            request.session['userid'] = request.POST["userid"]
            request.session['user_logged_in'] = "True"
            user_role = values[0]["role"]
            fname=values[0]["fname"]
            request.session['fname'] = fname
            if(values[0]["role"] == "chat_staff"):
                request.session['loggedin_user'] = "chat_staff"
                return redirect("/chat_staff")
            # print(fname)
            if(values[0]["role"] == "Admin" or values[0]["role"] == "Staff"):
                if (values[0]["role"] == "Admin" ):

                    request.session['loggedin_user'] = "Admin"
                else :
                    request.session['loggedin_user'] = "Staff"
                role = request.session['loggedin_user']
                isalready = Complaints.objects.filter().values()
                values = list(isalready)
                complain_count = Complaints.objects.all().count()
                resolved_count = Complaints.objects.filter(
                    status='resolved').count()
                pending_count = Complaints.objects.filter(
                    status='pending').count()
                in_progress_count = Complaints.objects.filter(
                    status='in_process').count()
                print(role)
                context  = {
                "test" : "Success",
                "user_logged_in": "True",
                "user_role":"admin",
                "complaints":values,
                "c_count":complain_count,
                "r_count":resolved_count,
                "p_count":pending_count,
                "ip_count": in_progress_count,
                'role': role
                }
            
                return redirect("/dashboard",context)

            else: 
                request.session['loggedin_user'] = "User"
                role = request.session['loggedin_user']
                context  = {
                    "test" : "Success",
                    "user_logged_in": "True",
                    "userid": request.POST["userid"],
                    'role':role
                }
            
                
                return render(request,"home.html",{"context": context})
        
    if request.method == 'GET':
        
        if 'user_logged_in' in request.session:
            if (request.session['user_logged_in'] == "True"): 
                pass
            else: 
                return render(request,"login.html",{ "message" : message })
        else: 
            return render(request,"login.html",{ "message" : message })
        
def registeruser(request):

    message = ""
    
    if request.method == 'POST':
        criterion1 = Q(userid =  request.POST["email"]) #any query you want
        isalready = User.objects.filter(criterion1).values()
        values = list(isalready)
        if(len(values)==0):

            #otp process
            


            data_to_add = User(
            userid = request.POST["email"],
            password = request.POST["password"],
            role = "User",
            fname= request.POST["fname"],
            lname= request.POST["lname"],
            email = request.POST["email"],

            )

            data_to_add.save()
        
            
            return render(request,"login.html",{"context": "Registration Successful"})
            
        else:
            message = "This user is already registered"
            return JsonResponse(message, safe=False)

           
        
    if request.method == 'GET':
        return render(request,"registeruser.html",{ "message" : message })


def forgot_password(request):
    if request.method == 'GET':
        
        return render(request,"forgot_password.html",)
    
    if request.method == 'POST':
        email=request.POST["email"]

        criterion1 = Q(userid =  request.POST["email"]) #any query you want
        isalready = User.objects.filter(criterion1).values()
        values = list(isalready)
        if(len(values)==0):
            message="The email you entered is not registered.Please check email."
            return render(request,"forgot_password.html",{"message":message})

        letters = string.ascii_lowercase
        password = ''.join(random.choice(letters) for i in range(6))
        message="Your Temporary Password is:\n"+password
        
        criterion1 = Q(userid =  request.POST["email"]) #any query you want
        isalready_user = User.objects.get(criterion1)
        isalready_user.password = password
        isalready_user.save()

        with get_connection(  
            host=settings.EMAIL_HOST, 
            port=settings.EMAIL_PORT,  
            username=settings.EMAIL_HOST_USER, 
            password=settings.EMAIL_HOST_PASSWORD, 
            use_tls=settings.EMAIL_USE_TLS
        ) as connection:  
            subject = "Temporary Password for FairHire"
            email_from = settings.EMAIL_HOST_USER  
            recipient_list = [email, ]  
            message = message 
            EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()  

        message_success="New password has been sent to your email account use that password and login again."
        return render(request,"forgot_password.html",{"message_success":message_success})        





def home(request): 
    if request.method == 'GET':
        # print(request.session['userid'])
        if 'user_logged_in' in request.session:


            role = request.session['loggedin_user']
            print(role)
            context  = {
                    "user_logged_in": request.session['user_logged_in'],
                    "userid": request.session['userid'],
                    'role':role
            }
            return render(request,"home.html",{ "context" : context })
        else:

            message = "WELCOME TO HOMEPAGE"
            return render(request,"home.html",{ "message" : message })

def laws(request): 
    if request.method == 'GET':

        if 'user_logged_in' in request.session:
            role = request.session['loggedin_user']

            context  = {
                    "user_logged_in": request.session['user_logged_in'],
                    "userid": request.session['userid'],
                    'role': role
            }
            return render(request,"laws.html",{ "context" : context })
        else:

            message = "WELCOME TO HOMEPAGE"
            return render(request,"laws.html",{ "message" : message })
       

def about(request): 
    if request.method == 'GET':
        if 'user_logged_in' in request.session:
            role = request.session['loggedin_user']

            context  = {
                    "user_logged_in": request.session['user_logged_in'],
                    "userid": request.session['userid'],
                    'role': role

            }
            return render(request,"about.html",{ "context" : context })
        else:

            message = "WELCOME TO HOMEPAGE"
            return render(request,"about.html",{ "message" : message })
        
        

def new_complaint(request): 
    if request.method == 'GET':

        logged_user_details = userloggedin(request)
        if(logged_user_details["userid"] == ""):
            return render(request,"login.html")
        else: 
            context  = {
                    "user_logged_in": request.session['user_logged_in'],
                    "userid": logged_user_details["userid"],
                    'role': logged_user_details["loggedin_user"]
            }
            return render(request,"new_complaint.html",{ "context" : context })
        


def complaint(request): 
    if request.method == 'GET':
        logged_user_details = userloggedin(request)
        if(logged_user_details["userid"] == ""):
            return render(request,"login.html")
        else: 
            
            criterion1 = Q(userid =  logged_user_details['userid']) #any query you want
            isalready = Complaints.objects.filter(criterion1).values()
            values = list(isalready)
            
            context  = {
                    "user_logged_in": request.session['user_logged_in'],
                    "userid": logged_user_details['userid'],
                    "complaints":values
            }
            return render(request,"complaint.html",{ "context" : context })
        

    if request.method == 'POST':
        # complaint = Complaints.objects.get(pk=complaint_id)
        
        staff_users = User.objects.filter(role='Staff')
        complaints_count = {}
        for user in staff_users:
            complaints_count[user.userid] = Complaints.objects.filter(
                assigniduserid=user.userid).count()
        
        min_complaints = min(complaints_count.values())
        least_complaints_users = [
            userid for userid, count in complaints_count.items() if count == min_complaints]
        assigned_user_id = least_complaints_users[randint(
            0, len(least_complaints_users)-1)]
        print(assigned_user_id)
        assigned_user = User.objects.get(email=assigned_user_id)
   
        # complaint.save()
    # return HttpResponseRedirect(reverse('complaints_list'))
        data_to_add = Complaints(
            firstname = request.POST["firstname"],
            lastname = request.POST["lastname"],
            mobile = request.POST["mobile"],
            email = request.session['userid'],
            type_of_disability = request.POST["type_of_disability"],
            description = request.POST["description"],
            company = request.POST["company"],
            city = request.POST["city"],
            state = request.POST["state"],
            pincode = request.POST["pincode"],
            date = request.POST["date"],
            userid = request.session['userid'],
            assigniduserid=assigned_user
        )


        # complaint.assigniduserid = assigned_user_id
        data_to_add.save()

        criterion1 = Q(userid =  request.session['userid']) #any query you want
        isalready = Complaints.objects.filter(criterion1).values()
        values = list(isalready)
      
        context  = {
                "user_logged_in": request.session['user_logged_in'],
                "userid": request.session['userid'],
                "complaints":values
        }

        ###sending confirmation mail function calling
        
        send_email(request)
        return render(request, "complaint.html", {"context": context})

##email confirmation fucntion
def send_email(request):

    email=request.session['userid']
    type_of_disability = request.POST["type_of_disability"]
    company = request.POST["company"]
    date = request.POST["date"]
    message="This email is to notify you that the compaint of "+type_of_disability +" you filed against the company "+company+" has been filed on date "+date+".\n"

    if request.method == "POST": 
       with get_connection(  
            host=settings.EMAIL_HOST, 
            port=settings.EMAIL_PORT,  
            username=settings.EMAIL_HOST_USER, 
            password=settings.EMAIL_HOST_PASSWORD, 
            use_tls=settings.EMAIL_USE_TLS  
        ) as connection:  
            subject = "Complaint confirmation."
            email_from = settings.EMAIL_HOST_USER  
            recipient_list = [email, ]  
            message = message 
            EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()  
 
    return render(request, 'home.html')


