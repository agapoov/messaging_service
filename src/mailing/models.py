from django.core.validators import RegexValidator
from django.db import models


class Client(models.Model):
    phone_regex = RegexValidator(
        regex=r'^7\d{10}$',
        message='The phone number must be in the format: "7XXXXXXXXXX" '
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=11,
        unique=True
    )
    operator_code = models.CharField(max_length=3)
    tag = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.operator_code:
            self.operator_code = self.phone_number[1:4]
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Клиент {self.phone_number}'


class Mailing(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    message_text = models.TextField()
    filter_params = models.JSONField(default=dict)

    class Meta:
        ordering = ['-start_time']


class Message(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='messages')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f'Сообщение для {self.client}'
