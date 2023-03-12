from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest
from datetime import datetime
# from django.views.generic import TemplateView
from django.db.models import Count
from .models import PasswordReset
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.urls import reverse
import requests
import openai
from django.shortcuts import render
from django.http import JsonResponse

from django.http import JsonResponse

# from product_analysis.models import Caps, Decoration, Material, Shape, platforms, user, files, Formats
from fairhireapp.models import Complaints

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
        print("use:", message)
        # print("in2")
        # prompt = message
        prompt = f"give me brief answer of {message} \n"
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
    isalready = Complaints.objects.filter().values()
    values = list(isalready)
    complain_count = Complaints.objects.all().count()
    resolved_count = Complaints.objects.filter(
        status='resolved').count()
    pending_count = Complaints.objects.filter(
        status='pending').count()
    in_progress_count = Complaints.objects.filter(
        status='in_process').count()
    print(request.user)
    context  = {
    "test": "Success",
    "user_logged_in": "True",
    "user_role":"admin",
    "complaints":values,
    "c_count":complain_count,
    "r_count":resolved_count,
    "p_count":pending_count,
    "ip_count": in_progress_count
    }
    return render(request, "dashboard.html", {"context": context})


def complain_details(request,id):
    context=Complaints.objects.get(id=id)
    return render(request, 'user_complain_details.html', {'context': context})


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
    print(cities,status)
    context = {
        "test": "Success",
        "user_logged_in": "True",
        "user_role": "admin",
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
   
