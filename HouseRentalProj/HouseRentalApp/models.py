from django.db import models
from django.contrib.auth.models import User
# Create your models here.
Allowed_for = (
    ('all','All'),
    ('couple', 'Couple'),
    ('bachelor(male)','Bachelor(Male)'),
    ('bachelor(female)','Bachelor(Female)'),
    ('family','Family'),
)
room_type = (
    ('1bhk','1BHK'),
    ('2bhk', '2BHK'),
    ('3bhk', '3BHK'),
    ('4bhk', '4BHK'),
    ('single room', 'Single Room'),
    ('double room', 'Double Room'),
    ('whole house','Whole House'),
)

class House(models.Model):
    houseName = models.CharField(max_length=100,blank=True,null=True)
    ownerName = models.CharField(max_length=100)
    phone = models.IntegerField()
    address = models.CharField(max_length=100)
    landmark = models.CharField(max_length=150,blank=True,null=True)
    city = models.CharField(max_length=50)
    rent = models.IntegerField()
    description = models.TextField(max_length=400,blank=True, null=True)
    allowed = models.CharField(max_length=50, choices=Allowed_for, default='all')
    roomType = models.CharField(max_length=25, choices=room_type, default='single room')
    building_img = models.ImageField(upload_to='images/')
    bedroom_img = models.ImageField(upload_to='images/')
    kitchen_img = models.ImageField(upload_to='images/')
    bathroom_img = models.ImageField(upload_to='images/')
    favorite = models.ManyToManyField(User, related_name='favorite')

    def __str__(self):
        return self.houseName

class Review(models.Model):
    review = models.TextField(max_length=200,blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='house')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
