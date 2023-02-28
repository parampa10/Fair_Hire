from django.urls import path,include

from . import views
from fairhireapp.backend import login,complaint, home, about, laws, registeruser, logout
# from product_analysis.apidata import complaint, home,login, signup, customize, save, toedit, edit, show_files,data,show_product, show_all_product, delete, getCardData, formSave

urlpatterns = [

    path('',home),
    path('login',login),
    path('complaint',complaint),
    path('about',about),
    path('laws',laws),
    path('registeruser',registeruser),
    path('logout', logout),
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

