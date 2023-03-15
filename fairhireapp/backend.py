from random import randint
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
    print("Hello")
    if request.method == 'POST':
        print("Hello")
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
            
            # request.session['role'] = request.POST["userid"]
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
                return render(request,"dashboard.html",{"context": context})

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

            data_to_add = User(
            userid = request.POST["email"],
            password = request.POST["password"],
            role = "User",
            email = request.POST["email"],

            )

            data_to_add.save()
        
            
            return render(request,"login.html",{"context": "Registration Successful"})
            
        else:
            message = "This user is already registered"
            return JsonResponse(message, safe=False)

           
        
    if request.method == 'GET':
        return render(request,"registeruser.html",{ "message" : message })
    
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
        message = "WELCOME TO HOMEPAGE"
        if 'user_logged_in' in request.session:
            role = request.session['loggedin_user']

            
            context  = {
                    "user_logged_in": request.session['user_logged_in'],
                    "userid": request.session['userid'],
                    'role': role
            }
            return render(request,"new_complaint.html",{ "context" : context })
        else:

            message = "WELCOME TO HOMEPAGE"
            return render(request,"new_complaint.html",{ "message" : message })


def complaint(request): 
    if request.method == 'GET':
        message = "WELCOME TO HOMEPAGE"
        if 'user_logged_in' in request.session:
            
            criterion1 = Q(userid =  request.session['userid']) #any query you want
            isalready = Complaints.objects.filter(criterion1).values()
            values = list(isalready)
           
            context  = {
                    "user_logged_in": request.session['user_logged_in'],
                    "userid": request.session['userid'],
                    "complaints":values
            }
            return render(request,"complaint.html",{ "context" : context })
        else:

            message = "WELCOME TO HOMEPAGE"
            return render(request,"complaint.html",{ "message" : message })
        

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
            email = request.POST["email"],
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
        return render(request, "complaint.html", {"context": context})


    


