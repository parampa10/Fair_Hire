import string
from django.core.validators import MinLengthValidator
import random
from django.db import models
from datetime import timedelta
from django.utils import timezone
class User(models.Model):
    userid = models.CharField(primary_key = True, max_length=100)
    email = models.EmailField(null=True)
    role = models.CharField( max_length=100)
    fname = models.CharField( max_length=100)
    lname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return str(self.userid)
    
class User_Logged(models.Model):
    userid = models.CharField(primary_key = True, max_length=100)

    def __str__(self):
        return str(self.userid)
    

class Complaints(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('in_process', 'In Process'),
    )
    id = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    type_of_disability = models.CharField(null=True, max_length=100)
    description = models.TextField(null=True)
    company = models.CharField(null=True, max_length=100)
    city = models.CharField(null=True,max_length=100)
    state = models.CharField(null=True,max_length=100)
    pincode = models.CharField(null=True,max_length=100)
    date = models.CharField(max_length=100 , null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    assigniduserid = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    complaint_token = models.CharField(max_length=8, unique=True, validators=[MinLengthValidator(8)])
    comment = models.TextField(null=True)




class ChatRoom(models.Model):
    assigned_to = models.ForeignKey(
        User, related_name='chat_assignments', on_delete=models.CASCADE)
    requester = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Chat room {self.id} assigned to {self.assigned_to}'

    def resolve(self):
            # delete all messages associated with this chat room
            self.messages.all().delete()
            # delete the chat room itself
            self.delete()
            
class ChatMessage(models.Model):
    chat_room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} in chat room {self.chat_room.id}'


# class PasswordReset(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     token = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def is_valid(self):
#         return timezone.now() <= self.created_at + timedelta(hours=24)









# Create your models here.
# class user(models.Model):
#     userid = models.CharField(primary_key = True, max_length=100)
#     password = models.CharField(max_length=100)

#     def __str__(self):
#         return str(self.userid)

# class files(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     platform = models.CharField(max_length=100)
#     brand = models.CharField(max_length=100)
#     userid = models.ForeignKey(user,on_delete=models.CASCADE)
#     work = models.TextField(null=True)
#     decorations = models.TextField(null=True)
#     format = models.TextField(null=True)
#     shape = models.TextField(null=True)
#     cap = models.TextField(null=True)
#     material = models.TextField(null=True)
#     min_time = models.CharField(max_length=100 , null=True)
#     max_time = models.CharField(max_length=1000 , null=True)
#     min_cost = models.CharField(max_length=1000 , null=True)
#     max_cost = models.CharField(max_length=1000 , null=True)
#     ul_capex = models.CharField(max_length=1000 , null=True)
#     sustainability = models.CharField(max_length=1000 , null=True)
#     sample_readiness = models.CharField(max_length=1000 , null=True)
#     all_items = models.TextField(null=True)



#     type = models.CharField(max_length=1000 , null=True)

#     def __str__(self):
#         return str(self.id)

# class Decoration(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=1000 , null=True)
#     min_time = models.CharField(max_length=1000 , null=True)
#     max_time = models.CharField(max_length=1000 , null=True)
#     baseline = models.CharField(max_length=1000 , null=True)
#     min_cost = models.CharField(max_length=1000 , null=True)
#     max_cost = models.CharField(max_length=1000 , null=True)
#     ul_capex = models.CharField(max_length=1000 , null=True)
#     consumer_benefit = models.CharField(max_length=1000 , null=True)
#     sustainability = models.CharField(max_length=1000 , null=True)
#     design_code = models.CharField(max_length=1000 , null=True)
#     sample_readiness = models.CharField(max_length=1000 , null=True)
#     src = models.TextField(max_length=1000 , null=True)
#     related_shapes = models.TextField( null=True)
#     related_caps = models.TextField( null=True)
#     related_laminate = models.TextField(null=True)
#     type = models.CharField(max_length=1000 )
    
           
#     def __str__(self):
#         return str(self.id)


# class Material(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=1000 , null=True)
#     min_time = models.CharField(max_length=1000 , null=True)
#     max_time = models.CharField(max_length=1000 , null=True)
#     baseline = models.CharField(max_length=1000 , null=True)
#     min_cost = models.CharField(max_length=1000 , null=True)
#     max_cost = models.CharField(max_length=1000 , null=True)
#     ul_capex = models.CharField(max_length=1000 , null=True)
#     consumer_benefit = models.CharField(max_length=1000 , null=True)
#     sustainability = models.CharField(max_length=1000 , null=True)
#     design_code = models.CharField(max_length=1000 , null=True)
#     sample_readiness = models.CharField(max_length=1000 , null=True)
#     src = models.TextField(max_length=1000 , null=True)
#     related_shapes = models.TextField( null=True)
#     related_caps = models.TextField( null=True)
#     related_decorations = models.TextField(null=True)
#     type = models.CharField(max_length=1000 )
           
#     def __str__(self):
#         return str(self.id)

# class Shape(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=1000 , null=True)
#     min_time = models.CharField(max_length=1000 , null=True)
#     max_time = models.CharField(max_length=1000 , null=True)
#     baseline = models.CharField(max_length=1000 , null=True)
#     min_cost = models.CharField(max_length=1000 , null=True)
#     max_cost = models.CharField(max_length=1000 , null=True)
#     ul_capex = models.CharField(max_length=1000 , null=True)
#     consumer_benefit = models.CharField(max_length=1000 , null=True)
#     sustainability = models.CharField(max_length=1000 , null=True)
#     design_code = models.CharField(max_length=1000 , null=True)
#     sample_readiness = models.CharField(max_length=1000 , null=True)
#     src = models.TextField(max_length=1000 , null=True)
#     related_decorations = models.TextField( null=True)
#     related_caps = models.TextField( null=True)
#     related_laminate = models.TextField(null=True)
#     type = models.CharField(max_length=1000)
           
#     def __str__(self):
#         return str(self.id)

# class Formats(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=1000 , null=True)
#     min_time = models.CharField(max_length=1000 , null=True)
#     max_time = models.CharField(max_length=1000 , null=True)
#     min_cost = models.CharField(max_length=1000 , null=True)
#     max_cost = models.CharField(max_length=1000 , null=True)
#     ul_capex = models.CharField(max_length=1000 , null=True)
#     consumer_benefit = models.CharField(max_length=1000 , null=True)
#     sustainability = models.CharField(max_length=1000 , null=True)
#     design_code = models.CharField(max_length=1000 , null=True)
#     sample_readiness = models.CharField(max_length=1000 , null=True)
#     src = models.TextField(max_length=1000 , null=True)
#     type = models.CharField(max_length=1000 , default="Format")
           
#     def __str__(self):
#         return str(self.id)

# class Caps(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=1000 , null=True)
#     min_time = models.CharField(max_length=1000 , null=True)
#     max_time = models.CharField(max_length=1000 , null=True)
#     baseline = models.CharField(max_length=1000 , null=True)
#     min_cost = models.CharField(max_length=1000 , null=True)
#     max_cost = models.CharField(max_length=1000 , null=True)
    
#     ul_capex = models.CharField(max_length=1000 , null=True)
#     consumer_benefit = models.CharField(max_length=1000 , null=True)
#     sustainability = models.CharField(max_length=1000 , null=True)
#     design_code = models.CharField(max_length=1000 , null=True)
#     sample_readiness = models.CharField(max_length=1000 , null=True)
#     src = models.TextField(max_length=1000 , null=True)
#     related_shapes = models.TextField( null=True)
#     related_decorations = models.TextField( null=True)
#     related_laminate = models.TextField(null=True)
#     type = models.CharField(max_length=1000)
           
#     def __str__(self):
#         return str(self.id)

# class platforms(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=40)
#     brand = models.CharField(max_length=100)
           
#     def __str__(self):
#         return str(self.id)
