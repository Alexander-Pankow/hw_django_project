from django.db import models
# from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now


"""
HW16
Домашнее задание: 
Реализация CRUD для категорий с использованием ModelViewSet, мягкое удаление.
Реализовать полный CRUD для модели категорий (Categories) с помощью ModelViewSet,
 добавить кастомный метод для подсчета количества задач в каждой категории.
  Реализовать систему мягкого удаления для категорий.

Задание 1: Реализация CRUD для категорий с использованием ModelViewSet
Шаги для выполнения:
Создайте CategoryViewSet, используя ModelViewSet для CRUD операций.
Добавьте маршрут для CategoryViewSet.
Добавьте кастомный метод count_tasks используя декоратор @action
 для подсчета количества задач, связанных с каждой категорией.

Задание 2: Реализация мягкого удаления категорий
Шаги для выполнения:
Добавьте два новых поля в вашу модель Category, если таких ещё не было.
В модели Category добавьте поля is_deleted(Boolean, default False) 
и deleted_at(DateTime, null=true)
Переопределите метод удаления, чтобы он обновлял новые поля к соответствующим значениям:
 is_deleted=True и дата и время на момент “удаления” записи
Переопределите менеджера модели Category
В менеджере модели переопределите метод get_queryset(),
 чтобы он по умолчанию выдавал только те записи, которые не “удалены” из базы.
"""


class SoftDeleteManager(models.Manager):
    """Менеджер для исключения удалённых записей"""
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Category(models.Model):

    """Категория выполнения"""

    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')
    is_deleted = models.BooleanField(default=False, verbose_name="Удалена?")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата удаления")

    objects = SoftDeleteManager()  # по умолчанию — только активные
    all_objects = models.Manager()  # полный доступ (включая удалённые)

    def delete(self, using=None, keep_parents=False):
        """Мягкое удаление"""
        self.is_deleted = True
        self.deleted_at = now()
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'                      # имя таблицы
        verbose_name = 'Category'                               # человеко читаемое имя
        verbose_name_plural = 'Categories'                      # множественное число
        ordering = ['name']                                     # сортировка по названию
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_category_name')
        ]

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

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'              # имя таблицы
        verbose_name = 'Task'                       # человеко читаемое имя
        verbose_name_plural = 'Tasks'               # множественное число
        ordering = ['-created_at']                  # сортировка: сначала новые
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique_task_title')
        ]

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

    class Meta:
        db_table = 'task_manager_subtask'                         # имя таблицы
        verbose_name = 'SubTask'                                  # человеко читаемое имя
        verbose_name_plural = 'SubTasks'                          # множественное число
        ordering = ['-created_at']                                # сортировка: сначала новые
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique_subtask_title')
        ]


# class TimeStampedModel(models.Model):
#     """
#     Abstract model that provides created_at and updated_at timestamps.
#     """
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
#     updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))
#
#     class Meta:
#         abstract = True