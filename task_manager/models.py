from django.db import models


class Category(models.Model):

    """Категория выполнения"""

    name = models.CharField(max_length=100, unique=True,verbose_name='Название категории')

    def __str__(self):
        return self.name

STATUS_CHOICES = [
        ('New', 'New'),
        ('In progress', 'In progress'),
        ('Pending', 'Pending'),
        ('Blocked', 'Blocked'),
        ('Done', 'Done'),
    ]

class Task(models.Model):

    """Задача для выполнения."""

    title = models.CharField(max_length=100,verbose_name='Название задачи')
    description = models.TextField(blank=True,verbose_name='Описание задачи')
    categories = models.ManyToManyField(Category, related_name='tasks',verbose_name='Категории задачи')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New',verbose_name=' Статус задачи')
    deadline = models.DateTimeField(verbose_name='Дата и время дедлайн')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Дата и время создания')

    class Meta:
        unique_together = ('title', 'deadline')  # Название уникально для даты

    def __str__(self):
        return self.title


class SubTask(models.Model):
    """Отдельная часть основной задачи (Task)"""

    title = models.CharField(max_length=100,verbose_name='Название подзадачи')
    description = models.TextField(blank=True,verbose_name='Описание подзадачи')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks',verbose_name='Основная задача')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New',verbose_name='Статус задачи')
    deadline = models.DateTimeField(verbose_name='Дата и время дедлайн')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Дата и время создания')

    def __str__(self):
        return f"{self.title} ({self.task.title})"