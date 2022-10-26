from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets ,status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Rating ,Meal
from .serializers import MealSerializer,RatingSerializer ,UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated ,AllowAny

class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    authentication_classes=(TokenAuthentication , )
    permission_classes = (AllowAny ,)
    
    def create(self,request,*args,**kwargs):
           serializer=self.get_serializer(data=request.data)
           serializer.is_valid(raise_exception=True)
           self.perform_create(serializer)
           token ,created=Token.objects.get_or_create(user=serializer.instance)
           return Response({'token':token.key},status=status.HTTP_201_CREATED)
    def list(self,request,*args,**kwargs):
        response={
            "message":'you cant create rating like that'
        }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)
       
    
class MealViewSet(viewsets.ModelViewSet):
    queryset=Meal.objects.all()
    serializer_class=MealSerializer
    authentication_classes=(TokenAuthentication , )
    permission_classes = (IsAuthenticated ,)
    
    @action(methods=["POST"],detail=True)
    def rate_meal(self,request,pk=None):
        if 'stars' in request.data:
            """ create or update"""
            meal=Meal.objects.get(id=pk)
            stars=request.data['stars']
            user=request.user
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
    authentication_classes=(TokenAuthentication , )
    permission_classes = (IsAuthenticated ,)
    
    def update(self,request,*args,**kwargs):
        response={
            'message':"this is not how you should create/update/rating"
        }
        return Response(response , status=status.HTTP_400_BAD_REQUEST)
    def create(self,request,*args,**kwargs):
        response={
            'message':"this is not how you should create/update/rating"
        }
        return Response(response , status=status.HTTP_400_BAD_REQUEST)