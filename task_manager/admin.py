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

"""
Задание 1:
Добавить настройку инлайн форм для админ класса задач. При создании задачи должна появиться возможность создавать сразу и подзадачу.
"""

class SubTaskInlineAdmin(admin.TabularInline):
    model = SubTask
    extra = 3

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'status', 'deadline', 'created_at')   # колонки для списка
    list_filter = ('status', 'categories')                         # фильтры по статусу и категориям
    search_fields = ('title', 'description')                       # поиск по заголовку и описанию
    ordering = ('-created_at',)                                    # сортировка по дате создания (новые сверху)
    filter_horizontal = ('categories',)                            # удобный выбор нескольких категорий
    inlines = [SubTaskInlineAdmin]                                 # для возможности добавления подзадач через Inline

    # Задание 2:
    # Названия задач могут быть длинными и ухудшать читаемость в Админ панели,
    # поэтому требуется выводить в списке задач укороченный вариант
    # первые 10 символов с добавлением «...», если название длиннее,
    # при этом при выборе задачи для создания подзадачи должно отображаться полное название.
    #  Необходимо реализовать такую возможность.

    def short_title(self, obj):
        if len(obj.title) > 10:
            return f"{obj.title[:10]}..."
        return obj.title

    short_title.short_description = "Task Title"  # Заголовок колонки

# Задание 3:
# Реализовать свой action для Подзадач,
# который поможет выводить выбранные в Админ панели объекты в статус Done

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
       list_display = ('title', 'task', 'status', 'deadline', 'created_at')
       list_filter = ('status', 'task')
       search_fields = ('title', 'description')
       ordering = ('-created_at',)

       actions = ["mark_done"]  # <-- указываем метод action в списке

       @admin.action(description='Mark selected subtasks as Done')
       def mark_done(self, request, queryset):
           # быстро обновляем статус всех выбранных подзадач одним запросом
           updated_count = queryset.update(status='Done')

           # показываем сообщение пользователю, что подзадача отмечена как выполненая
           self.message_user(request, f"{updated_count} subtasks marked as Done.")





