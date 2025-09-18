from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from django.db.models import Count
from .models import Task,SubTask
from .serializers import TaskSerializer,SubTaskCreateSerializer



@api_view(['POST'])
def task_create(request):
    """
    Задание 1: создание задачи
    """
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def task_list(request):
    """
     Задание 2: Получить список всех задач
    """
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def task_detail(request, pk):
    """
    Задание 2: Получить задачу по ID
    """
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def task_stats(request):
    """
    Задание 3: статистика задач
    - общее количество
    - количество по каждому статусу
    - количество просроченных задач
    """
    total = Task.objects.count()
    by_status = Task.objects.values('status').annotate(count=Count('status'))
    overdue = Task.objects.filter(deadline__lt=now()).count()

    data = {
        "total_tasks": total,
        "tasks_by_status": list(by_status),
        "overdue_tasks": overdue
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def task_update(request, pk):
    """
    Обновить задачу по ID
    """
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def task_delete(request, pk):
    """
    Удалить задачу по ID
    """
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    task.delete()
    return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# Задание 5: SubTask Views

class SubTaskListCreateView(APIView):
    """
    GET  -> список подзадач
    POST -> создать подзадачу
    """

    def get(self, request):
        subtasks = SubTask.objects.all()
        serializer = SubTaskCreateSerializer(subtasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):
    """
    GET    -> получить подзадачу
    PUT    -> обновить подзадачу
    DELETE -> удалить подзадачу
    """

    def get_object(self, pk):
        try:
            return SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return None

    def get(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response({"error": "SubTask not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubTaskCreateSerializer(subtask)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response({"error": "SubTask not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response({"error": "SubTask not found"}, status=status.HTTP_404_NOT_FOUND)
        subtask.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)