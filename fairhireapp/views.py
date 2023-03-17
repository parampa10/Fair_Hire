from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest
from datetime import datetime
from random import randint

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
from fairhireapp.models import Complaints, User, ChatMessage, ChatRoom
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
        prompt = f"give me brief answer related dicrimination {message} \n"
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
    role = request.session['loggedin_user']
    userid = request.session['userid']
    fname = request.session['fname']
    if role == 'Staff':
        isalready = Complaints.objects.filter(assigniduserid=userid).values()
        values = list(isalready)
        complain_count = Complaints.objects.filter(
            assigniduserid=userid).count()
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

    context = {
        "test": "Success",
        "user_logged_in": "True",
        "user_role": "admin",
        "complaints": values,
        "c_count": complain_count,
        "r_count": resolved_count,
        "p_count": pending_count,
        "ip_count": in_progress_count,
        "role": role,
        "fname": fname
    }
    # return JsonResponse({"context": context})
    return render(request, "dashboard.html", {"context": context})


def complain_details(request, id):
    data = Complaints.objects.get(id=id)

    context = {
        "user_logged_in": request.session['user_logged_in'],
        "userid": request.session['userid'],
        "role": request.session['loggedin_user']


    }

    if request.session['loggedin_user'] == "User":
        return render(request, 'my_complain_details.html', {'context': context, 'data': data})
    else: 
        return render(request, 'user_complain_details.html', {'context': context, 'data': data})


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
        "status": status,
        'status_counts': status_counts
    }
    # print(context)
    return render(request, 'statistics.html', {"context": context})


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
                userid=request.POST["email"],
                password=request.POST["password"],
                role=request.POST['role'],
                email=request.POST["email"],
                fname=request.POST["fname"],
                lname=request.POST["lname"]

            )

            data_to_add.save()
            context = {
                "message": "Registration Successful",
                "role": role
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

#chat_perpose


def chat_staff(request):
    role = request.session['loggedin_user']
    userid = request.session['userid']
    # fname, lname=
    # fname = request.session['fname']
    if role == 'chat_staff':
        isalready = ChatRoom.objects.filter(assigned_to=userid)
        values = list(isalready)

        chatroom = ChatRoom.objects.filter(assigned_to=userid).count()
        pending_count = ChatRoom.objects.filter(
            is_active=True).count()
        resolved_count = ChatRoom.objects.filter(
            is_active=False).count()

        context = {
            "user_logged_in": request.session['user_logged_in'],
            "userid": request.session['userid'],
            "role": request.session['loggedin_user'],
            'chats': values,
            "r_count": resolved_count,
            "p_count": pending_count,

        }
        return render(request, 'chat_staff.html', {'context': context})
    else:
        return render(request, 'login.html')


def chat_request(request):
    current_user_email = request.session['userid']
    current_user = User.objects.get(email=current_user_email)
    staff_users = User.objects.filter(role='chat_staff')
    chat_count = {}
    for user in staff_users:
        chat_count[user.userid] = ChatRoom.objects.filter(
            assigned_to=user.userid).count()

    min_chat = min(chat_count.values())
    least_chat_users = [
        userid for userid, count in chat_count.items() if count == min_chat]
    assigned_user_id = least_chat_users[randint(
        0, len(least_chat_users)-1)]
    assigned_user = User.objects.get(email=assigned_user_id)

    chat_room = ChatRoom.objects.create(
        assigned_to=assigned_user, requester=current_user)

    context = {
        "user_logged_in": request.session['user_logged_in'],
        "userid": request.session['userid'],
        "role": request.session['loggedin_user'],
        'chatroom': chat_room
    }
    return render(request, 'chat.html', {'context': context})


def staff_chat_room(request,id):
    chat_room = ChatRoom.objects.get(id=id)
    print(chat_room)
    context = {
        "user_logged_in": request.session['user_logged_in'],
        "userid": request.session['userid'],
        "role": request.session['loggedin_user'],
        'chatroom': chat_room
    }
    return render(request, 'chat.html', {'context': context})

def chat_message(request):
    if request.method == 'POST':
        chat_room_id = request.POST.get('chat_room_id')
        sender_id = request.POST.get('sender_id')
        message = request.POST.get('message')
        chat_room = ChatRoom.objects.get(id=chat_room_id)
        sender = User.objects.get(userid=sender_id)
        chat_message = ChatMessage.objects.create(
            chat_room=chat_room,
            sender=sender,
            message=message
        )
        print(chat_message)
        response_data = {
            'message': message,
            'sender': sender.email
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({})


def get_messages(request, id):
    role = request.session.get('loggedin_user')
    
    try:
        print("fuck")
        print(ChatRoom.objects.get(id=id))
        chat_room = ChatRoom.objects.get(id=id)
    except ChatRoom.DoesNotExist:
        messages = [{'sender': " From Other Side ", 'message': "chat closed"}]
        print(messages)
        return JsonResponse({'messages':list(messages)})
        return redirect('chat_staff' if role == 'chat_staff' else '/')
        # if role == "User":
        #     return redirect('')
        # elif role == "chat_staff":
        #     return redirect('chat_staff')
    messages = ChatMessage.objects.filter(
        chat_room=chat_room).values('sender', 'message')
    print(messages)
    return JsonResponse({'messages': list(messages)})


def resolved_chat(request, id):
    role = request.session.get('loggedin_user')
    userid = request.session.get('userid')
    try:
        chat_room = ChatRoom.objects.get(id=id)
    except ChatRoom.DoesNotExist:
        return redirect('chat_staff' if role == 'chat_staff' else '/')
    chat_room.is_active = False
    chat_room.save()
    chat_room.resolve()
    return redirect('chat_staff' if role == 'chat_staff' else '/')

# def get_messages(request, id):
#     role = request.session['loggedin_user']
#     userid = request.session['userid']
#     print(ChatRoom.objects.get(id=id))
#     try:
#         chat_room = ChatRoom.objects.get(id=id)
#         print(chat_room)
#     except ChatRoom.DoesNotExist:
#         if role == "User":
#             return redirect('')
#         else:
#             return redirect('chat_staff')
#     messages = ChatMessage.objects.filter(
#         chat_room=chat_room).values('sender', 'message')
#     print(messages)
#     return JsonResponse({'messages': list(messages)})




# def resolved_chat(request, id):
#     role = request.session['loggedin_user']
#     userid = request.session['userid']
#     # fname, lname=
#     # fname = request.session['fname']
#     if role == 'chat_staff':
#         chat_room = ChatRoom.objects.get(id=id)
#         chat_room.is_active = False
#         chat_room.save()
#         chat_room.resolve()
#         return redirect('chat_staff')
#     else:
#         chat_room = ChatRoom.objects.get(id=id)
#         chat_room.is_active = False
#         chat_room.save()
#         chat_room.resolve()
#         return redirect('/')
