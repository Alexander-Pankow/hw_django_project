from django.db.models.functions import ExtractWeekDay
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import filters,viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from django.db.models import Count
from .models import Task,SubTask,Category
from .serializers import TaskSerializer,SubTaskCreateSerializer,SubTaskSerializer,CategorySerializer

#HW16

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()  # по умолчанию только активные
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def count_tasks(self, request, pk=None):
        """Подсчёт задач в категории"""
        category = self.get_object()
        count = category.tasks.count()  # related_name='tasks' в Task
        return Response({'category': category.name, 'tasks_count': count})




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

class TaskListView(APIView):

    def get(self, request):
        """
            HW14
        Задание 1:
    Написать, или обновить, если уже есть, эндпоинт на получение списка всех задач по дню недели.
    Если никакой параметр запроса не передавался - по умолчанию выводить все записи.
    Если был передан день недели (например вторник) - выводить список задач только на этот день недели.
        """
        deadline = request.query_params.get('deadline', None)

        if deadline is not None:
            try:
                weekday = int(deadline)
                res = Task.objects.annotate(
                    weekday=ExtractWeekDay('deadline')
                ).filter(weekday=weekday)
            except ValueError:
                return Response(
                    {"error": "Deadline must be a number (1=Sunday, 2=Monday, ...7=Saturday)"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            res = Task.objects.all()

        serializer = TaskSerializer(res, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class SubTaskListView(APIView, PageNumberPagination):
    page_size = 5

    def get(self, request):
        """
            HW14
        Задание 2:
            Добавить пагинацию в отображение списка подзадач.
            На одну страницу должно отображаться не более 5 объектов.
            Отображение объектов должно идти в порядке убывания даты
            (от самого последнего добавленного объекта к самому первому)
        """
        subtasks = SubTask.objects.all().order_by('-created_at')  # сортировка по убыванию даты создания
        self.page_size = self.get_page_size(request)              # проверка параметра page_size (если захотим поменять через запрос)
        result = self.paginate_queryset(subtasks, request, view=self) # применяем пагинацию
        serializer = SubTaskSerializer(result, many=True)             # сериализация данных
        return self.get_paginated_response(serializer.data)

    def get_page_size(self, request):
        """
            Если в запросе есть параметр page_size и он число — используем его,
            иначе оставляем значение по умолчанию (5).
        """
        page_size = request.query_params.get('page_size', None)
        if page_size and page_size.isdigit():
            return int(page_size)
        return self.page_size


class SubTaskFilterListView(APIView, PageNumberPagination):
    page_size = 5  # максимум 5 подзадач на страницу

    def get(self, request):
        """
        HW14
        Задание 3:
    Добавить или обновить, если уже есть, эндпоинт на получение списка всех подзадач по названию главной задачи и статусу подзадач.
    Если фильтр параметры в запросе не передавались - выводить данные по умолчанию, с учётом пагинации.
    Если бы передан фильтр параметр названия главной задачи - выводить данные по этой главной задаче.
    Если был передан фильтр параметр конкретного статуса подзадачи - выводить данные по этому статусу.
    Если были переданы оба фильтра - выводить данные в соответствии с этими фильтрами.
        """


        subtasks = SubTask.objects.all().order_by('-created_at')             # берем все подзадачи

        task_title = request.query_params.get('task_title', None)  # достаем параметры фильтра из запроса
        status_filter = request.query_params.get('status', None)


        if task_title:
            subtasks = subtasks.filter(task__title__icontains=task_title)  # если фильтры есть — применяем
                                                                           # __icontains = поиск по подстроке (чтобы не зависело от регистра)
        if status_filter:
            subtasks = subtasks.filter(status=status_filter)

        self.page_size = self.get_page_size(request)                         # пагинация
        result = self.paginate_queryset(subtasks, request, view=self)

        serializer = SubTaskSerializer(result, many=True)                    # сериализация
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_page_size(self, request):
        """Поддержка изменения размера страницы через параметр ?page_size=N"""
        page_size = request.query_params.get('page_size', None)
        if page_size and page_size.isdigit():
            return int(page_size)
        return self.page_size

"""
HW15
Задание 1: Замена представлений для задач (Tasks) на Generic Views
Шаги для выполнения:
Замените классы представлений для задач на Generic Views:
Используйте ListCreateAPIView для создания и получения списка задач.
Используйте RetrieveUpdateDestroyAPIView для получения, обновления и удаления задач.
Реализуйте фильтрацию, поиск и сортировку:
Реализуйте фильтрацию по полям status и deadline.
Реализуйте поиск по полям title и description.
Добавьте сортировку по полю created_at.
"""
# Список + создание задач
class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']           # фильтрация
    search_fields = ['title', 'description']            # поиск
    ordering_fields = ['created_at']                    # сортировка


# Детали, обновление, удаление задачи
class TaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

"""
HW15
Задание 2: Замена представлений для подзадач (SubTasks) на Generic Views
Шаги для выполнения:
Замените классы представлений для подзадач на Generic Views:
Используйте ListCreateAPIView для создания и получения списка подзадач.
Используйте RetrieveUpdateDestroyAPIView для получения, обновления и удаления подзадач.
Реализуйте фильтрацию, поиск и сортировку:
Реализуйте фильтрацию по полям status и deadline.
Реализуйте поиск по полям title и description.
Добавьте сортировку по полю created_at.
"""

# Список + создание подзадач
class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']           # фильтрация
    search_fields = ['title', 'description']            # поиск
    ordering_fields = ['created_at']                    # сортировка


# Детали, обновление, удаление подзадачи
class SubTaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer