from django.utils import timezone

from celery import shared_task

from .models import Client, Mailing, Message


@shared_task
def send_message(client_id: int, mailing_id: int):
    client = Client.objects.get(id=client_id)
    mailing = Mailing.objects.get(id=mailing_id)

    if timezone.now() > mailing.end_time:
        print(f'Mailing {mailing_id} expired')

    message = Message.objects.create(
        client=client,
        mailing=mailing
    )
    message.save()
    print(f"""
    {'*'*50}
    Отправлено сообщение:
    Текст: {mailing.message_text}
    Клиент: {client.phone_number}
    Время: {message.created_at}
    {'*'*50}
    """)


@shared_task
def sending_processing(mailing_id: int):
    mailing = Mailing.objects.get(id=mailing_id)

    if timezone.now() > mailing.end_time:
        print(f'Mailing {mailing_id} expired')
        return

    # filters = {}
    # filter_operator_code = mailing.filter_params.get('operator_code')
    # filter_tag = mailing.filter_params.get('tag')
    # if filter_operator_code:
    #     filters['operator_code'] = filter_operator_code
    # if filter_tag:
    #     filters['tag'] = filter_tag
    filters = {}
    if mailing.filter_params.get('operator_code'):
        filters['operator_code'] = mailing.filter_params['operator_code']
    if mailing.filter_params.get('tag'):
        filters['tag'] = mailing.filter_params['tag']

    clients = Client.objects.filter(**filters)

    for client in clients:
        send_message.delay(client.id, mailing_id)
