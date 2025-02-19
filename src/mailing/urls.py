from django.urls import path
from .views import MailingCreateView, MailingDetailView, MailingListView

urlpatterns = [
    path('', MailingListView.as_view(), name='mailing-list'),
    path('<int:pk>/', MailingDetailView.as_view(), name='mailing-detail'),
    path('create/', MailingCreateView.as_view(), name='mailing-create'),

]
