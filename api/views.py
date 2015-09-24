from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

def get_serializer(app_name,class_):
  serializers = __import__(app_name+".serializers",fromlist=['serializers'])
  return getattr(serializers,class_)

@api_view(['GET', 'POST'])
def list_view(request,app_name,class_):
  model = serializer.Meta.model
  if request.method == 'GET':
    flags = model.objects.all()
    serializer = serializer(flags, many=True)
    return Response(serializer.data)

  elif request.method == 'POST':
    serializer = serializer(data=request.DATA)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def detail_view(request,app_name,class_,pk):
  model = serializer.Meta.model
  try:
    flag = model.objects.get(pk=pk)
  except model.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = serializer(flag)
    return Response(serializer.data)

  elif request.method == 'PUT':
    serializer = serializer(flag, data=request.DATA)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

  elif request.method == 'DELETE':
    flag.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
