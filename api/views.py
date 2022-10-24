from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets ,status
from django.contrib.auth.models import User
from .models import Rating ,Meal
from .serializers import MealSerializer,RatingSerializer


class MealViewSet(viewsets.ModelViewSet):
    queryset=Meal.objects.all()
    serializer_class=MealSerializer
    
    @action(methods=["POST"],detail=True)
    def rate_meal(self,request,pk=None):
        if 'stars' in request.data:
            """ create or update"""
            meal=Meal.objects.get(id=pk)
            username=request.data['username']
            stars=request.data['stars']
            user=User.objects.get(username=username)
            try:
                #update
                rateing=Rating.objects.get(user=user.id,meal=meal.id)
                rateing.stars=stars
                rateing.save()
                serializer =RatingSerializer(rateing,many=False)
                json={
                    "message":"rating updated " ,
                    "result" : serializer.date
                }
                return Response(json)
            except:
                #create rating if it dose not exist
                rateing=Rating.objects.create(user=user,meal=meal, stars=stars)
                serializer =RatingSerializer(rateing,many=False)
                json={
                    "message":"rating created" ,
                    "result" : serializer.data
                }
                
                return Response(json ,status=status.HTTP_200_OK)
        else:
            json ={
                "message":'stars not provided'
            }
            return Response( status=status.HTTP_400_BAD_REQUEST)

class RatingViewSet(viewsets.ModelViewSet):
    queryset=Rating.objects.all()
    serializer_class=RatingSerializer