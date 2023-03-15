from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest
from datetime import datetime
# from django.views.generic import TemplateView
from django.db.models import Count
# from .models import PasswordReset
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
# from django.contrib.auth.models import User
from fairhireapp.models import Complaints, User
# from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.urls import reverse
import requests
import openai
from django.shortcuts import render
from django.http import JsonResponse

from django.shortcuts import redirect

# user=User.objects.get()

# Set up the OpenAI API key and model
openai.api_key = "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"
model_engine = "text-davinci-003"


def chatbot(request):
    """
    A view that handles the chatbot functionality.
    """
    if request.method == 'POST':
        #message = request.POST["user_msg"]
        message = request.POST.get('message', '')
        #message = request.POST.get('user_msg', '')
        # print(request.POST)
        print("user:", message)
        # print("in2")
        # prompt = message
        prompt = f"give me brief answer related to dicrimination for {message} \n"
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Extract the AI's response from the OpenAI API response
        response_text = response.choices[0].text.strip()
        response_text = response_text.replace("AI:", "").strip()
        print(response_text)
        # Return the response as JSON
        # response = chatbot_response(message)
        return JsonResponse({'res': response_text})
        return render(request, "home.html", {"res": response_text})
        # return JsonResponse({'res': response_text})

    return JsonResponse({'error': 'Invalid request.'})



def change_status(request, pk):
    complaint = get_object_or_404(Complaints, pk=pk)
    new_status = request.POST.get('status')
    print(new_status)
    if new_status in ('resolved', 'in_process', 'pending'):
        complaint.status = new_status
        complaint.save()
        return redirect('dashboard')
        # return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponseBadRequest('Invalid status')
        # return redirect(reverse('dashboard'),context)
    
    # context = {"complaint": complaint}
    # return render(request, "dashboard.html", {"context": context})
    # return render(request,"dashboard.html",{"context": values})


def dashboard(request):
    # values = Complaints.objects.all().order_by('date')
    # isalready = Complaints.objects.filter().values()
    # values = list(isalready)
    if (request.session['user_logged_in'] == "True"):
        role = request.session['loggedin_user']
        userid = request.session['userid']
        fname = request.session['fname']
        if role == 'Staff':
            isalready = Complaints.objects.filter(assigniduserid=userid).values()
            values = list(isalready)
            complain_count = Complaints.objects.filter(assigniduserid=userid).count()
            resolved_count = Complaints.objects.filter(
                assigniduserid=userid, status='resolved').count()
            pending_count = Complaints.objects.filter(
                assigniduserid=userid, status='pending').count()
            in_progress_count = Complaints.objects.filter(
                assigniduserid=userid, status='in_process').count()
        else:
            isalready = Complaints.objects.all()
            values = list(isalready)

            complain_count = Complaints.objects.all().count()
            resolved_count = Complaints.objects.filter(
                status='resolved').count()
            pending_count = Complaints.objects.filter(
                status='pending').count()
            in_progress_count = Complaints.objects.filter(
                status='in_process').count()
    
   
   
        context  = {
        "test": "Success",
        "user_logged_in": "True",
        "user_role":"admin",
        "complaints":values,
        "c_count":complain_count,
        "r_count":resolved_count,
        "p_count":pending_count,
        "ip_count": in_progress_count,
        "role":role,
        "fname":fname
        }
        # return JsonResponse({"context": context})
        return render(request, "dashboard.html", {"context": context})

    else: 
        return render(request, "login.html")


def complain_details(request,id):
    data=Complaints.objects.get(id=id)
    context  = {
                    "user_logged_in": request.session['user_logged_in'],
                    "userid": request.session['userid'],
                    "role": request.session['loggedin_user']
                    

            }
    return render(request, 'user_complain_details.html', {'context': context, 'data': data })


# --------------------------------------------------------------------------------
# rom django.shortcuts import render, redirect
def Statistics(request):
    city_counts = Complaints.objects.values(
        'city').order_by().annotate(count=Count('city'))
    cities = [city_count['city'] for city_count in city_counts]
    object_counts = [city_count['count'] for city_count in city_counts]

    state_counts = Complaints.objects.values(
        'state').order_by().annotate(count=Count('state'))
    states = [state_count['state'] for state_count in state_counts]
    state_counts = [state_count['count'] for state_count in state_counts]

    company_counts = Complaints.objects.values(
        'company').order_by().annotate(count=Count('company'))
    companies = [company_count['company']
                 for company_count in company_counts]
    company_counts = [company_count['count']
                      for company_count in company_counts]
    status_counts = Complaints.objects.values(
        'status').order_by().annotate(count=Count('status'))
    status = [status_counts['status'] for status_counts in status_counts]
    status_counts = [status_counts['count']
                     for status_counts in status_counts]
    role = request.session['loggedin_user']
    context = {
        "test": "Success",
        "user_logged_in": "True",
        "role": role,
        'cities': cities,
        'object_counts': object_counts,
        'states': states,
        'state_counts': state_counts,
        'companies': companies,
        'company_counts': company_counts,
        "status":status,
        'status_counts': status_counts
    }
    # print(context)
    return render(request, 'statistics.html', {"context":context})


def newuser(request):

    message = ""
    
    
            
    
    if request.method == 'POST':
        role = request.session['loggedin_user']
        criterion1 = Q(userid=request.POST["email"])  # any query you want
        isalready = User.objects.filter(criterion1).values()
        values = list(isalready)
        
        if(len(values) == 0):

            print(request.POST['role'])

            data_to_add = User(
            userid = request.POST["email"],
            password = request.POST["password"],
            role=request.POST['role'],
            email = request.POST["email"],
            fname=request.POST["fname"],
            lname=request.POST["lname"]

            )

            data_to_add.save()
            context={
                "message": "Registration Successful",
                "role":role
            }
            return render(request, "newuser.html", {"context": context})

        else:
            message = "This user is already registered"
            return JsonResponse(message, safe=False)

           
        
    if request.method == 'GET':
      if 'user_logged_in' in request.session:
            role = request.session['loggedin_user']
            context = {
                "user_logged_in":  request.session['user_logged_in'],
                "role": role
            }
            return render(request, "newuser.html", {"context": context})
# def newuser(request):


    # return render(request, "newuser.html", {"context": "Registration Successful"})
  
    # if request.method == 'GET':
        # return render(request, "registeruser.html", {"message": message})
