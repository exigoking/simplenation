from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer,UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions

# Needed this before Response, that apperently already handles JSON part
# class JSONResponse(HttpResponse):
#     """
#     An HttpResponse that renders its content into JSON.
#     """
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)



# @api_view(['GET','POST'])
# def snippet_list(request, format=None):
class SnippetList(generics.ListCreateAPIView):
    """
    List all code snippets, or create a new snippet.
    """
    queryset = Snippet.objects.all()
    serializer_class=SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
	# def perform_create(self, serializer):
	# 	serializer.save(owner=self.request.user)
    def get(self, request, format=None):
		snippets = Snippet.objects.all()
		serializer = SnippetSerializer(snippets, many=True)
		return Response(serializer.data)

    
    def post(self, request, format=None):
	    serializer = SnippetSerializer(data=request.data)
	    if serializer.is_valid():
	        serializer.save(owner=self.request.user)
	        return Response(serializer.data, status=status.HTTP_201_CREATED)
	    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a code snippet.
    """
    queryset = Snippet.objects.all()
    serializer_class=SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # def get_object(self, pk):
    # 	try:
    #  	   snippet = Snippet.objects.get(pk=pk)
   	# 	except Snippet.DoesNotExist:
    #     	return Response(status=status.HTTP_404_NOT_FOUND)

    # def get(self, request, pk, format=None):
    # 	snippet = self.get_object(pk)
    #     serializer = SnippetSerializer(snippet)
    #     return Response(serializer.data)

    # def put(self, request, pk, format = None):
    # 	snippet = self.get_object(pk)
    #     serializer = SnippetSerializer(snippet, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    # 	snippet = self.get_object(pk)
    #     snippet.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class UserList(generics.ListAPIView):
 	queryset = User.objects.all()
 	serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
 	queryset = User.objects.all()
 	serializer_class = UserSerializer