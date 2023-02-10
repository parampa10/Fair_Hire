from django.db import models




class Complaints(models.Model):
    id = models.AutoField(primary_key=True)
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
