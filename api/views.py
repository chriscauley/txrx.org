from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

def get_serializer(app_name,class_):
  serializers = __import__(app_name+".serializers",fromlist=['serializers'])
  return getattr(serializers,class_)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def list_view(request,app_name,class_,serializer=None):
  serializer = serializer or get_serializer(app_name,class_)
  model = serializer.Meta.model
  if hasattr(serializer,'permissions') and not serializer.permissions(request):
    return Response(status=status.HTTP_401_UNAUTHORIZED)
  if request.method == 'GET':
    serializer = serializer(request, many=True)
    return serializer.get_paginated_response()

  elif request.method == 'POST':
    serializer = serializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def detail_view(request,app_name,class_,pk,serializer=None):
  serializer = serializer or get_serializer(app_name,class_)
  model = serializer.Meta.model
  if hasattr(serializer,'permissions') and not serializer.permissions(request):
    return Response(status=status.HTTP_401_UNAUTHORIZED)
  try:
    item = model.objects.get(pk=pk)
  except model.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = serializer(item)
    return Response(serializer.data)

  elif request.method == 'PUT':
    serializer = serializer(item, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

  elif request.method == 'DELETE':
    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
