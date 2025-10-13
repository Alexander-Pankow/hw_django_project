from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Task

@receiver(pre_save, sender=Task)
def notify_on_status_change(sender, instance, **kwargs):
    """
    Если статус изменился и он отличается от last_notified_status — отправляем email
    (в тесте — печать в консоль при EMAIL_BACKEND = console)
    """
    if not instance.pk:
        # новая задача — не шлём
        return
    try:
        prev = Task.objects.get(pk=instance.pk)
    except Task.DoesNotExist:
        return

    old_status = prev.status
    new_status = instance.status

    if old_status != new_status:
        # проверка: уже не уведомляли про этот статус ранее?
        if prev.last_notified_status == new_status:
            # уже уведомляли ранее о переходе в этот статус — пропускаем
            return

        # отправка письма (console backend выведет в консоль)
        subject = f'Task "{instance.title}" status changed'
        message = f'Your task "{instance.title}" changed status from "{old_status}" to "{new_status}".'
        recipient = [instance.owner.email] if instance.owner.email else None
        if recipient:
            send_mail(subject, message, None, recipient)
        else:
            # если email нет — всё равно напечатать в консоль через send_mail (it will go to console backend)
            send_mail(subject, message, None, ['admin@example.com'])

        # обновим поле last_notified_status на инстанции, чтобы миграция/сохранение выставило новое значение
        instance.last_notified_status = new_status