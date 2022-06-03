from django import forms
from .models import House, Review
class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['houseName','ownerName','phone','address','landmark','city','rent','description','allowed','roomType','building_img','bedroom_img','kitchen_img','bathroom_img']
class UploadForm(forms.Form):
    file  = forms.FileField()
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review']