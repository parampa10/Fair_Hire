from django.urls import path,include
from .views import change_password, chatbot
from .views import change_status
from .views import dashboard
from . import views
from fairhireapp.backend import login,complaint, home, about, laws, logout, new_complaint,forgot_password, searched_Complain
# from product_analysis.apidata import complaint, home,login, signup, customize, save, toedit, edit, show_files,data,show_product, show_all_product, delete, getCardData, formSave

urlpatterns = [

    path('',home),
    path('login',login),
    path('complaint',complaint),
    path('complaint/search', searched_Complain),

    path('new_complaint',new_complaint),
    path('forgot_password',forgot_password),
    path('complain_status/<int:pk>', change_status, name='change_status'),
    
    path('about',about),
    path('laws',laws),
#     path('registeruser',registeruser),
    path('logout', logout),
    
    path('statistics', views.Statistics),
    path('complain_details/<int:id>',
         views.complain_details, name='complain_details'),
    path('complain_details_staff/<int:id>',
         views.complain_details_staff, name='complain_details_staff'),

    path('chatbot', chatbot, name='chatbot'),
    path('dashboard',dashboard, name='dashboard'),
    path('change_password',change_password, name='change_password'),
    path('chat_staff', views.chat_staff, name='chat_staff'),
    path('newuser', views.newuser),
   
    path('chat_request', views.chat_request),
#     path('chat_user', views.chat_user),

    path('get_messages/<int:id>', views.get_messages),
    path('resolved_chat/<int:id>', views.resolved_chat, name="resolved_chat"),
    path('chat_message', views.chat_message, name='chat_message'),
    path('chat_staff/staff_chat_room/<int:id>', views.staff_chat_room, name='staff_chat_room'),
    path('add_comment/<int:complaint_id>',
         views.add_comment, name='add_comment'),
    path('delete_comment/<int:complaint_id>/',
         views.delete_comment, name='delete_comment'),
    path('delete_complaint/<int:complaint_id>/',
         views.delete_complaint, name='delete_complaint'),


    # path('addnewuser',views.addnewuser)

    
    # path('login',login),
    # path('signup',signup),
    # path('customize/<str:userid>',customize, name="customize"),
    # path('home/<str:userid>',customize),
    # path('editfile/<str:userid>/<str:fileid>/<str:platform>/<str:brand>/<str:type>',toedit, name="namedurl"),
    # path('save/',save),
    # path('sort/',data),
    # path('edit/',edit),
    # path('files/<str:userid>',show_files, name="showfiles"),
    # path('product/<str:id>/<str:userid>',show_product),
    # path('items/<str:userid>/<str:brand>/<str:bookmark>',show_all_product),
    # path('delete/<str:fileid>', delete),
    # path('getCardData/', getCardData),
    # path('formSave', formSave)
    


]

