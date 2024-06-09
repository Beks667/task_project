from django.db import models
from apps.accounts.models import CustomUser


class Task(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True,
                             verbose_name='Пользователь')
    title = models.CharField(max_length=200, verbose_name='Название', )
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
