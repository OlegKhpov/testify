from rest_framework import generics

from testify.api.serializers import TestSerializer
from testify.models import Test


class TestListCreateView(generics.ListCreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class TestUpdateDeleteView(generics.RetrieveUpdateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class TestDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
