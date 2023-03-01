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
    
    return render(request,"login.html")

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
            print("Hello")
            return JsonResponse(message, safe=False)
        else:
            message = "login successful"
            request.session['userid'] = request.POST["userid"]
            request.session['user_logged_in'] = "True"
            
            if(values[0]["role"] == "Admin"):
                request.session['loggedin_user'] = "Admin"
                
                isalready = Complaints.objects.filter().values()
                values = list(isalready)
                
                
                context  = {
                "test" : "Success",
                "user_logged_in": "True",
                "userid": request.POST["userid"],
                "complaints":values
                }
            
                
                return render(request,"dashboard.html",{"context": context})

            else: 
                request.session['loggedin_user'] = "User"
            
                context  = {
                    "test" : "Success",
                    "user_logged_in": "True",
                    "userid": request.POST["userid"]

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
            role = "user",
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
            context  = {
                    "user_logged_in": request.session['user_logged_in'],
                    "userid": request.session['userid']

            }
            return render(request,"home.html",{ "context" : context })
        else:

            message = "WELCOME TO HOMEPAGE"
            return render(request,"home.html",{ "message" : message })

def laws(request): 
    if request.method == 'GET':

        if 'user_logged_in' in request.session:
            context  = {
                    "user_logged_in": request.session['user_logged_in'],
                    "userid": request.session['userid']

            }
            return render(request,"laws.html",{ "context" : context })
        else:

            message = "WELCOME TO HOMEPAGE"
            return render(request,"laws.html",{ "message" : message })
       

def about(request): 
    if request.method == 'GET':
        if 'user_logged_in' in request.session:
            context  = {
                    "user_logged_in": request.session['user_logged_in'],
                    "userid": request.session['userid']

            }
            return render(request,"about.html",{ "context" : context })
        else:

            message = "WELCOME TO HOMEPAGE"
            return render(request,"about.html",{ "message" : message })
        
        

def new_complaint(request): 
    if request.method == 'GET':
        message = "WELCOME TO HOMEPAGE"
        if 'user_logged_in' in request.session:
            
            
            context  = {
                    "user_logged_in": request.session['user_logged_in'],
                    "userid": request.session['userid'],
                    
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
            print(values)
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
            userid = request.session['userid']
        )

        data_to_add.save()

        criterion1 = Q(userid =  request.session['userid']) #any query you want
        isalready = Complaints.objects.filter(criterion1).values()
        values = list(isalready)
        print(values)
        context  = {
                "user_logged_in": request.session['user_logged_in'],
                "userid": request.session['userid'],
                "complaints":values
        }
        return render(request,"complaint.html",{ "context" : context })

        
    
    


# def login(request):

#     message = ""
    
#     if request.method == 'POST':
#         criterion1 = Q(userid =  request.POST["userid"]) #any query you want
#         criterion2 = Q(password=request.POST["password"]) #any query you want
#         isalready = user.objects.filter(criterion1 & criterion2 ).values()
#         values = list(isalready)
    
#         if(len(values)==0):
#             message = "This user is not registered"
#             return JsonResponse(message, safe=False)
#         else:
#             message = "login successful"
#             decorations = list(Decoration.objects.all().values())
#             caps = list(Caps.objects.all().values())
#             shapes = list(Shape.objects.all().values())
#             materials = list(Material.objects.all().values())
#             formats  = list(Formats.objects.all().values())
            
#             context  = {
#                 "test" : "Success",
#                 "userid": request.POST["userid"],
#                 "decorations": decorations,
#                 "caps": caps,
#                 "shapes": shapes,
#                 "materials": materials,
#                 "formats": formats
#             }
        
            
#             return render(request,"customize.html",{"context": context})

           
        
#     if request.method == 'GET':
#         return render(request,"login.html",{ "message" : message })
        
   
# def formSave(request):
      
#     if request.method == 'POST':

#         related_decorations = listToString(request.POST.getlist("decorations[]"))
#         related_shapes = listToString(request.POST.getlist("shapes[]"))
#         related_caps = listToString(request.POST.getlist("caps[]"))
#         related_materials = listToString(request.POST.getlist("materials[]"))
        
#         folder = os.path.join(settings.BASE_DIR, 'product_analysis/static/image/')   
        
#         myfile = request.FILES['image']       
#         fs = FileSystemStorage(location=folder) #defaults to   MEDIA_ROOT  
#         name = myfile.name.replace(",", " ", 50)
#         filename = fs.save(name, myfile)
        

#         if request.POST["selected_table"] == 'Caps':
#                 data_to_add = Caps(
#                     name = request.POST["name"],
#                     min_time = request.POST["min_time"],
#                     max_time = request.POST["max_time"],
#                     min_cost = request.POST["min_cost"],
#                     max_cost = request.POST["max_cost"],
#                     ul_capex = request.POST["ul_capex"],
#                     consumer_benefit = request.POST["consumer_benefit"],
#                     sustainability = request.POST["sustainability"],
#                     design_code = request.POST["design_code"],
#                     sample_readiness = request.POST["sample_readiness"],
#                     src = filename,
#                     related_shapes = related_shapes,
#                     related_decorations = related_decorations,
#                     related_laminate = related_materials,
#                     type = "Caps & Closure"
#                 )

#                 data_to_add.save()

#         elif request.POST["selected_table"] == 'Decorations':
#                 data_to_add = Decoration(
#                     name = request.POST["name"],
#                     min_time = request.POST["min_time"],
#                     max_time = request.POST["max_time"],
#                     min_cost = request.POST["min_cost"],
#                     max_cost = request.POST["max_cost"],
#                     ul_capex = request.POST["ul_capex"],
#                     consumer_benefit = request.POST["consumer_benefit"],
#                     sustainability = request.POST["sustainability"],
#                     design_code = request.POST["design_code"],
#                     sample_readiness = request.POST["sample_readiness"],
#                     src = filename,
#                     related_shapes = related_shapes,
#                     related_caps = related_caps,
#                     related_laminate = related_materials,
#                     type = "Printing & Decoration"
#                 )

#                 data_to_add.save()

#         elif request.POST["selected_table"] == 'Shapes':
#                 data_to_add = Shape(
#                     name = request.POST["name"],
#                     min_time = request.POST["min_time"],
#                     max_time = request.POST["max_time"],
#                     min_cost = request.POST["min_cost"],
#                     max_cost = request.POST["max_cost"],
#                     ul_capex = request.POST["ul_capex"],
#                     consumer_benefit = request.POST["consumer_benefit"],
#                     sustainability = request.POST["sustainability"],
#                     design_code = request.POST["design_code"],
#                     sample_readiness = request.POST["sample_readiness"],
#                     src = filename,
#                     related_decorations = related_decorations,
#                     related_caps = related_caps,
#                     related_laminate = related_materials,
#                     type = "Shape"
#                 )

#                 data_to_add.save()

#         elif request.POST["selected_table"] == 'Materials':
#                 data_to_add = Material(
#                     name = request.POST["name"],
#                     min_time = request.POST["min_time"],
#                     max_time = request.POST["max_time"],
#                     min_cost = request.POST["min_cost"],
#                     max_cost = request.POST["max_cost"],
#                     ul_capex = request.POST["ul_capex"],
#                     consumer_benefit = request.POST["consumer_benefit"],
#                     sustainability = request.POST["sustainability"],
#                     design_code = request.POST["design_code"],
#                     sample_readiness = request.POST["sample_readiness"],
#                     src = filename,
#                     related_decorations = related_decorations,
#                     related_caps = related_caps,
#                     related_shapes = related_shapes,
#                     type = "Laminate Material"
#                 )

#                 data_to_add.save()
        
#         elif request.POST["selected_table"] == 'Formats':
#                 data_to_add = Shape(
#                     name = request.POST["name"],
#                     min_time = request.POST["min_time"],
#                     max_time = request.POST["max_time"],
#                     min_cost = request.POST["min_cost"],
#                     max_cost = request.POST["max_cost"],
#                     ul_capex = request.POST["ul_capex"],
#                     consumer_benefit = request.POST["consumer_benefit"],
#                     sustainability = request.POST["sustainability"],
#                     design_code = request.POST["design_code"],
#                     sample_readiness = request.POST["sample_readiness"],
#                     src = filename,
#                     related_decorations = related_decorations,
#                     related_caps = related_caps,
#                     related_laminate = related_materials,
#                     type = "Format"
#                 )

#                 data_to_add.save()
                
                
#         context  = {
#             "message" : "Success"
#         }
#         return render(request,"formSave.html",{"context": context})
    
#     if request.method == 'GET':

#         decorations = list(Decoration.objects.all().values())
#         caps = list(Caps.objects.all().values())
#         shapes = list(Shape.objects.all().values())
#         materials = list(Material.objects.all().values())
#         formats = list(Formats.objects.all().values())


#         context  = {
#             "test" : "Success",
#             # "userid": userid,
#             "decorations": decorations,
#             "caps": caps,
#             "shapes": shapes,
#             "materials": materials,
#             "formats": formats
#         }

#         message = "test"
#         return render(request,"formSave.html",{ "message" : message,"context": context  })

# def signup(request):

#     message = ""
    
#     if request.method == 'POST':
#         criterion1 = Q(userid=request.POST["userid"])
#         isalready = user.objects.filter(criterion1).values()
#         values = list(isalready)
        
        
#         if(len(values)!=0):
#             message = "This userid is already registered"
#             return render(request,"signup.html",{ "message" : message })
#         else:
#             data_to_add = user(
#             userid = request.POST["userid"],
#             password = request.POST["password"],
#             )

#             data_to_add.save()
#             message = "Registered Succesfully."
#             return redirect('/login')
            
        
        
#     if request.method == 'GET':
#         return render(request,"signup.html",{ "message" : message })
        
    
# def show_files(request, userid):

#     criterion1 = Q(userid=userid) #any query you want
    
#     isalready = files.objects.filter(criterion1).values()
#     items = list(isalready)
    
#     for each in items:
#         temp = []
#         # if(each["type"] == "normal")
#         each["all_items"] = json.loads(each["all_items"])
#         each["cap"] = json.loads(each["cap"])
#         each["shape"] = json.loads(each["shape"])
#         each["material"] = json.loads(each["material"])
#         # each["format"] = json.loads(each["format"])
#         for item in each["all_items"]:
#             temp.append(each["all_items"][item])
#         each["all_items"] = temp
    

#     return render(request,"user.html",{ "context": {"userid":userid }, "files": items, "userid":userid })

# def show_all_product(request, userid, bookmark, brand):

#     criterion1 = Q(brand=brand) #any query you want
    
#     isalready = files.objects.filter(criterion1).values()
#     items = list(isalready)
    
#     for each in items:
#         temp = []
#         each["all_items"] = json.loads(each["all_items"])
#         each["cap"] = json.loads(each["cap"])
#         each["shape"] = json.loads(each["shape"])
#         each["material"] = json.loads(each["material"])
#         each["format"] = json.loads(each["format"])
#         for item in each["all_items"]:
#             temp.append(each["all_items"][item])
#         each["all_items"] = temp
    
#     if(brand == "closeup"):
#         return render(request,"closeup.html",{ "files": items, "userid":userid,"context": {"userid":userid }   })
#     elif(brand == "smile"):
#          return render(request,"smile.html",{ "files": items, "userid":userid ,"context": {"userid":userid } })



# def Convert(string):
#     li = list(string.split(","))
#     return li

# def show_product(request, id, userid):
#     criterion1 = Q(id=id) #any query you want
#     isalready = files.objects.filter(criterion1).values()
#     items = list(isalready)
    
    
#     temp = []
#     items[0]["all_items"] = json.loads(items[0]["all_items"])
#     items[0]["cap"] = json.loads(items[0]["cap"])
#     items[0]["shape"] = json.loads(items[0]["shape"])
#     items[0]["material"] = json.loads(items[0]["material"])
#     items[0]["format"] = json.loads(items[0]["format"])
#     for item in items[0]["all_items"]:
#         temp.append(items[0]["all_items"][item])
#     items[0]["all_items"] = temp
    

#     return render(request,"product_page.html",{ "context":{"userid": userid}, "files": items , "userid": userid})
    
# @api_view(['GET', 'POST', 'DELETE'])
# def data(request):
#     if request.method == 'POST':
        
#         if(request.POST["parameter"] == "2"):
#             decorations = list(Decoration.objects.filter(Q(max_time = request.POST["parameter"]) | Q(max_time = "1")).values())
#             caps = list(Caps.objects.filter(Q(max_time = request.POST["parameter"]) | Q(max_time = "1")).values())
#             shapes = list(Shape.objects.filter(Q(max_time = request.POST["parameter"]) | Q(max_time = "1")).values())
#             materials = list(Material.objects.filter(Q(max_time = request.POST["parameter"]) | Q(max_time = "1")).values())
#             formats = list(Formats.objects.filter(Q(max_time = request.POST["parameter"]) | Q(max_time = "1")).values())
#         elif(request.POST["parameter"] == "5"):
#             decorations = list(Decoration.objects.filter(Q(max_time = "5") | Q(max_time = "2")  | Q(max_time = "1")).values())
#             caps = list(Caps.objects.filter(Q(max_time = "5") | Q(max_time = "2") | Q(max_time = "1")).values())
#             shapes = list(Shape.objects.filter(Q(max_time = "5") | Q(max_time = "2") | Q(max_time = "1")).values())
#             materials = list(Material.objects.filter(Q(max_time = "5") | Q(max_time = "2") | Q(max_time = "1")).values())
#             formats = list(Formats.objects.filter(Q(max_time = "5") | Q(max_time = "2") | Q(max_time = "1")).values())
#         else:    
#             decorations = list(Decoration.objects.all().values())
#             caps = list(Caps.objects.all().values())
#             shapes = list(Shape.objects.all().values())
#             materials = list(Material.objects.all().values())
#             formats = list(Formats.objects.all().values())
#         # print(decorations)
        
        
#         return JsonResponse({"caps": caps, "decorations": decorations, "shapes": shapes, "materials": materials, "formats": formats}, safe=False)


# def customize(request, userid):
    

#     decorations = list(Decoration.objects.all().values())
#     caps = list(Caps.objects.all().values())
#     shapes = list(Shape.objects.all().values())
#     materials = list(Material.objects.all().values())
#     formats = list(Formats.objects.all().values())


#     context  = {
#         "test" : "Success",
#         "userid": userid,
#         "decorations": decorations,
#         "caps": caps,
#         "shapes": shapes,
#         "materials": materials,
#         "formats": formats
#     }
   
#     if request.method == 'GET':
#         return render(request,"customize.html",{"context": context})
    
        
    
# @api_view(['GET', 'POST', 'DELETE'])
# def save(request):
      
#     if request.method == 'POST':

        

#             decoration = json.loads(request.POST["decoration"])
#             print(decoration)

#             temp = []
#             for key in decoration:
#                 temp.append(decoration[key])

#             criterion1 = Q(userid =  request.POST["userid"]) 
#             criterion2 = Q(name=request.POST["filename"]) 
#             criterion3 = Q(brand=request.POST["brand"])
#             criterion4 = Q(platform=request.POST["platform"])
#             isalready = files.objects.filter((criterion1 & criterion2) & (criterion3 & criterion4) ).values()
#             values = list(isalready)
#             temp = listToString(temp)
            
        
#             if(len(values)==0):
#                 details = {
#                     "decoration": temp, 
#                     "shape": request.POST["shape"], 
#                     "cap": request.POST["cap"],
#                     "material": request.POST["material"],
#                     "format":request.POST["format"]
#                 }
#                 details = json.dumps(details)
#                 sustainability = ""
#                 ul_capex = "No"
#                 items = {}
#                 item_num = 0
#                 selected_decoration = []
#                 list_decoration = Convert(temp)
#                 for each in list_decoration:
#                     temp = list(Decoration.objects.filter(Q(id=each)).values())
#                     if(temp[0]["ul_capex"] == "Yes"):
#                         ul_capex = "Yes"
#                     items[str(item_num)] =  temp[0]
#                     item_num = item_num + 1
#                     selected_decoration.append(json.dumps(temp[0]))

                
#                 selected_decoration = listToString(selected_decoration)
                
#                 selected_shape = list(Shape.objects.filter(Q(id=request.POST["shape"])).values())
#                 if(selected_shape[0]["ul_capex"] == "Yes"):
#                         ul_capex = "Yes"

#                 selected_format = list(Shape.objects.filter(Q(id=request.POST["format"])).values())
#                 if(selected_format[0]["ul_capex"] == "Yes"):
#                         ul_capex = "Yes"
                
#                 selected_cap = list(Caps.objects.filter(Q(id=request.POST["cap"])).values())
#                 if(selected_cap[0]["ul_capex"] == "Yes"):
#                         ul_capex = "Yes"
                
#                 selected_material = list(Material.objects.filter(Q(id=request.POST["material"])).values())
#                 if(selected_material[0]["ul_capex"] == "Yes"):
#                         ul_capex = "Yes"
                
#                 instance_userid = user.objects.only('userid').get(userid=request.POST["userid"])
#                 items[str(item_num)] = (selected_shape[0])
#                 item_num = item_num + 1
#                 items[str(item_num)] = (selected_cap[0])
#                 item_num = item_num + 1
#                 items[str(item_num)] = (selected_material[0])
#                 item_num = item_num + 1
#                 items[str(item_num)] = (selected_format[0])

#                 selected_cap[0] = json.dumps(selected_cap[0])
#                 selected_material[0] = json.dumps(selected_material[0])
#                 selected_shape[0] = json.dumps(selected_shape[0])
#                 selected_format[0] = json.dumps(selected_format[0])
#                 items = json.dumps(items)

#                 print(selected_format[0])
        
#                 data_to_add = files(
#                 userid = instance_userid,
#                 name = request.POST["filename"],
#                 work = details,
#                 platform = request.POST["platform"],
#                 brand = request.POST["brand"],
#                 min_time = request.POST["min_time"],
#                 max_time = request.POST["max_time"],
#                 min_cost = request.POST["min_cost"],
#                 max_cost = request.POST["max_cost"],
#                 decorations = selected_decoration,
#                 cap = selected_cap[0],
#                 shape = selected_shape[0],
#                 material = selected_material[0],
#                 format = selected_format[0],
#                 ul_capex = ul_capex, 
#                 all_items = items, 
#                 type = request.POST["type"]
#                 )

#                 data_to_add.save()
#                 return JsonResponse("message", safe=False)
#             else:
#                 message = "Name already Exists"
#                 return JsonResponse(message, safe=False)

        
 
# # converts orders string from database to list to append new orders 
# def Convert(string):
#     li = list(string.split(","))
#     return li
# # converts upated list to string to add into database
# def listToString(s): 
#     str1 = "," 
#     return (str1.join(s)) 

# def toedit(request,userid,fileid, platform, brand, type):

#     context  = {
#         "test" : "Success"
#     }



#     decorations = list(Decoration.objects.all().values())
#     caps = list(Caps.objects.all().values())
#     shapes = list(Shape.objects.all().values())
#     materials = list(Material.objects.all().values())
#     # formats = list(Formats.objects.all().values())
   
    
#     criterion1 = Q(userid =  userid) #any query you want
#     criterion2 = Q(id= fileid) #any query you want
#     isalready = files.objects.filter(criterion1 & criterion2 ).values()
#     values = list(isalready)

#     values[0]["work"] = json.loads(values[0]["work"])

#     options = {
#         "decorations": decorations,
#         "caps": caps,
#         "shapes": shapes,
#         "materials": materials,
#         # "formats": formats
#     }

#     selected_decoration = []
#     list_decoration = Convert(values[0]["work"]["decoration"])
#     for each in list_decoration:
#         temp = list(Decoration.objects.filter(Q(id=each)).values())
#         selected_decoration.append(temp[0])

#     # selected_decoration = list(Decoration.objects.filter(Q(id=)).values())
#     selected_shape = list(Shape.objects.filter(Q(id=values[0]["work"]["shape"])).values())
#     selected_cap = list(Caps.objects.filter(Q(id=values[0]["work"]["cap"])).values())
#     selected_material = list(Material.objects.filter(Q(id=values[0]["work"]["material"])).values())
#     # selected_format = list(Formats.objects.filter(Q(id=values[0]["work"]["format"])).values())
    
#     context = {
#             # "message": values[0], 
#             "userid":values[0]["userid_id"],
#             "filename": values[0]["name"],
#             "decoration": selected_decoration,
#             "shape": selected_shape[0]["src"],
#             "cap": selected_cap[0]["src"],
#             "material": selected_material[0]["src"],
#             # "format":selected_format[0]["src"],
#             "decorationid": selected_decoration[0]["id"],
#             "shapeid": selected_shape[0]["id"],
#             "capid": selected_cap[0]["id"],
#             "materialid": selected_material[0]["id"],
#             # "formatid":selected_format[0]["id"],
#             "context": options, 
#             "platform": values[0]["platform"],
#             "brand": values[0]["brand"], 
#             "type": type
#     }
#     return render(request,"edit.html",{"context": context})

    
# @api_view(['GET', 'POST', 'DELETE'])
# def edit(request):
        
#     if request.method == 'POST':

#         criterion1 = Q(userid =  request.POST["userid"]) #any query you want
#         criterion2 = Q(name=request.POST["filename"]) #any query you want
#         # print(request.POST["filename"])
#         # print(request.POST["userid"])
        
#         isalready = files.objects.filter(criterion1 & criterion2 ).values()
#         values = list(isalready)

#         decoration = json.loads(request.POST["decoration"])
#         temp = []
#         for key in decoration:
#             temp.append(decoration[key])
#         temp = listToString(temp)

#         if(len(values)!=0):
#             details = {
#                 "decoration": temp, 
#                 "shape": request.POST["shape"], 
#                 "cap": request.POST["cap"],
#                 "material": request.POST["material"],
#                 # "format": request.POST["format"]
#             }
#             # print(details)
#             details = json.dumps(details)
#             selected_decoration = []
#             items = {}
#             ul_capex = "No"
#             item_num = 0
#             list_decoration = Convert(temp)
#             for each in list_decoration:
#                 temp = list(Decoration.objects.filter(Q(id=each)).values())
#                 if(temp[0]["ul_capex"] == "Yes"):
#                     ul_capex = "Yes"
#                 selected_decoration.append(json.dumps(temp[0]))
#                 items[str(item_num)] =  temp[0]
#                 item_num = item_num + 1

            
#             selected_decoration = listToString(selected_decoration)
            
#             selected_shape = list(Shape.objects.filter(Q(id=request.POST["shape"])).values())
#             if(selected_shape[0]["ul_capex"] == "Yes"):
#                     ul_capex = "Yes"

#             #  = list(Formats.objects.filter(Q(id=request.POST["format"])).values())
#             # if(selected_format[0]["ul_capex"] == "Yes"):
#             #         ul_capex = "Yes"selected_format
            
#             selected_cap = list(Caps.objects.filter(Q(id=request.POST["cap"])).values())
#             if(selected_cap[0]["ul_capex"] == "Yes"):
#                     ul_capex = "Yes"
            
#             selected_material = list(Material.objects.filter(Q(id=request.POST["material"])).values())
#             if(selected_material[0]["ul_capex"] == "Yes"):
#                     ul_capex = "Yes"
#             items[str(item_num)] = (selected_shape[0])
#             item_num = item_num + 1
#             items[str(item_num)] = (selected_cap[0])
#             item_num = item_num + 1
#             items[str(item_num)] = (selected_material[0])
#             item_num = item_num + 1
#             # items[str(item_num)] = (selected_format[0])
#             selected_cap[0] = json.dumps(selected_cap[0])
#             selected_material[0] = json.dumps(selected_material[0])
#             selected_shape[0] = json.dumps(selected_shape[0])
#             # selected_format[0] = json.dumps(selected_format[0])
            
#             items = json.dumps(items)
#             obj = files.objects.get(id=isalready[0]["id"])
                                       
#             obj.work = details
#             obj.min_time = request.POST["min_time"]
#             obj.max_time = request.POST["max_time"]
#             obj.min_cost = request.POST["min_cost"]
#             obj.max_cost = request.POST["max_cost"]
#             obj.decorations = selected_decoration
#             obj.cap = selected_cap[0]
#             obj.shape = selected_shape[0]
#             obj.material = selected_material[0]
#             obj.format = ""
#             obj.ul_capex = ul_capex
#             obj.all_items = items
            
#             obj.save()
                                
            
#             return JsonResponse("message", safe=False)
#         else:
#             message = "Name already Exists"
#             return JsonResponse(message, safe=False)

    
# def delete(request, fileid):

    
#     criterion1 = Q(id=fileid) #any query you want
#     # print("helllo", fileid)
#     files.objects.filter(criterion1).delete()
    
#     return JsonResponse("Done", safe=False)
    
# @api_view(['GET', 'POST', 'DELETE'])
# def getCardData(request):
#     if request.method == 'POST':
#         userId = request.POST["userId"]
#         brand = request.POST["brand"]
#         platform = request.POST["platform"]
#         # print(userId, brand, platform)
#         getData = list(files.objects.filter((Q(brand = brand) & Q(platform = platform)) & Q(userid = str(userId))).values())
#         # getData = list(files.objects.filter(Q(userid = userId)).values())
#         # getData = list(files.objects.all().values())
#         # print(getData)
#         getData = json.dumps(getData)
#         return JsonResponse(getData, safe=False)