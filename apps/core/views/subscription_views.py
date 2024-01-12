from ..serializers import SubscriptionSerializer, AttemptSerializer
from ..services.attempt_service import AttemptService
from ..models import Subscription
from rest_framework import status, permissions, mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response
import os
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class SubscriptionList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format = None):
        user = request.user
        subscriptions = user.subscription_set.all()
        serializer = SubscriptionSerializer(subscriptions,many=True)
        return Response(status=200,data= serializer.data)

    def post(self, request, format = None):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(owner=request.user)
                return Response(status=status.HTTP_201_CREATED,data=serializer.data)            
            except Exception as e:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE,data={"detail": "You have already subscribed to this OCR"})
        return Response(status=status.HTTP_400_BAD_REQUEST)

class AttemptList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, subscription_id, format = None):
        subscription = Subscription.objects.get(id=subscription_id)
        self.service = AttemptService(subscription) 
        if (subscription.usage_rate > subscription.plan.usage_limit):
            res = {"detail" : "You have exceeded your quota for this subscription"}
            sts = status.HTTP_406_NOT_ACCEPTABLE 
        else: 
            file = request.FILES.get("file")
            filepath =  os.path.join(settings.DOCUMENT_ROOT,file.name)
            with open(filepath, "wb") as f:
                f.write(file.read())
            res = self.service.create(filepath)
            sts = 201
        return Response(status=sts, data=res)
    
    def get(self,request, subscription_id, format= None):
        attempts = Subscription.objects.get(id=subscription_id).attempt_set.all()
        print(attempts)
        serializer = AttemptSerializer(attempts,many=True)
        return Response(status=201,data=serializer.data)
