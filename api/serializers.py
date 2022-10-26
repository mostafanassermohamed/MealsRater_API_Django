
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
       model=User
       fields=['id','username','password']
       extra_kwargs= {'password':{'write_only':True,'required':True}}
       

class MealSerializer(serializers.ModelSerializer):
    class Meta:
       model=Meal
       fields=['id','title','description', 'no_of_ratings','avg_rating']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
       model=Rating
       fields=['id','stars','user','meal']

    