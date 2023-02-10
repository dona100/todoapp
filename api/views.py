from multiprocessing import context
from django.shortcuts import render
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import ToDo
from api.serializers import ToDoSerializer,RegistrationSerializer
from django.contrib.auth.models import User
from rest_framework import permissions,authentication
# Create your views here.


class ToDoView(ViewSet):
    def list(self,request,*args,**kw):
        qs=ToDo.objects.all()
        serializer=ToDoSerializer(qs,many=True)
        return Response(data=serializer.data)

    def create(self,request,*args,**kw):
        serializer=ToDoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def retrieve(self,request,*args,**kw):
        id=kw.get("pk")
        qs=ToDo.objects.get(id=id)
        serializer=ToDoSerializer(qs,many=False)
        return Response(data=serializer.data)

    def destroy(self,request,*args,**kw):
        id=kw.get("pk")
        ToDo.objects.get(id=id).delete()
        return Response(data="deleted")

    def update(self,request,*args,**kw):
        id=kw.get("pk")
        object=ToDo.objects.get(id=id)
        serializer=ToDoSerializer(data=request.data,instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class ToDoModelView(ModelViewSet):
    # http_method_names=["get","post","put"]
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    serializer_class=ToDoSerializer
    queryset=ToDo.objects.all()

    def create(self,request,*args,**kw):
        serializer=ToDoSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    # def create(self, request, *args, **kwargs):
    #     serializer=ToDoSerializer(data=request.data)
    #     if serializer.is_valid():
    #         ToDo.objects.create(**serializer.validated_data,user=request.user)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)
    


    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    # def list(self,request,*args,**kw):
    #     qs=ToDo.objects.filter(user=request.user)
    #     serializer=ToDoSerializer(qs,many=True)
    #     return Response(data=serializer.data)
        


    @action(methods=["GET"],detail=False)
    def pending_todo(self,request,*args,**kw):
        qs=ToDo.objects.filter(status=False,user=self.request.user)
        serializer=ToDoSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    @action(methods=["GET"],detail=False)
    def completed_todo(self,request,*args,**kw):
        qs=ToDo.objects.filter(status=True)
        serializer=ToDoSerializer(qs,many=True)
        return Response(data=serializer.data)

    @action(methods=["POST"],detail=True)
    def mark_as_done(self,request,*args,**kw):
        id=kw.get("pk")
        object=ToDo.objects.get(id=id)
        object.status=True
        object.save()
        serializer=ToDoSerializer(object,many=False)
        return Response(data=serializer.data)

class UsersView(ModelViewSet):
    serializer_class=RegistrationSerializer
    queryset=User.objects.all()

    # def create(self,request,*args,**kw):
    #     serializer=RegistrationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         User.objects.create_user(**serializer.validated_data)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)



