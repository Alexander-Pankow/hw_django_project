from django.utils.timezone import now
from rest_framework.fields import DateTimeField
from rest_framework.serializers import ModelSerializer,ValidationError
from task_manager.models import Task,SubTask,Category

class TaskSerializer(ModelSerializer):
        class Meta:
            model = Task
            fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at']


# Задание 1: SubTaskCreateSerializer

class SubTaskCreateSerializer(ModelSerializer):
    created_at = DateTimeField(read_only=True) # не совсем понимаю

    class Meta:
        model = SubTask
        fields = "__all__"


# Задание 2: CategoryCreateSerializer

class CategoryCreateSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def validate_name(self, value):
        """Проверка уникальности имени"""
        qs = Category.objects.filter(name=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)  # исключаем текущую категорию при update
        if qs.exists():
            raise ValidationError("Категория с таким названием уже существует")
        return value

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance

# Задание 3: TaskDetailSerializer

class SubTaskSerializer(ModelSerializer):
    class Meta:
        model = SubTask
        fields = "__all__"


class TaskDetailSerializer(ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True, source="subtask_set")

    class Meta:
        model = Task
        fields = "__all__"

# Задание 4: TaskCreateSerializer

class TaskCreateSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def validate_deadline(self, value):
        if value < now():
            raise ValidationError("Дата дедлайна не может быть в прошлом")
        return value