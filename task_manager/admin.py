from django.contrib import admin
from .models import Category,Task,SubTask

# admin.site.register(Category)
# admin.site.register(Task)
# admin.site.register(SubTask)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)           # показывать колонку "Название"
    search_fields = ('name',)          # поиск по названию
    ordering = ('name',)               # сортировка по имени


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'created_at')   # колонки для списка
    list_filter = ('status', 'categories')                         # фильтры по статусу и категориям
    search_fields = ('title', 'description')                       # поиск по заголовку и описанию
    ordering = ('-created_at',)                                    # сортировка по дате создания (новые сверху)
    filter_horizontal = ('categories',)                            # удобный выбор нескольких категорий


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'task')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)