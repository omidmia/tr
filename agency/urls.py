from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    index,
    UserLoginView,
    VisaView,
    TicketView,
    RenewView,
    TransactionView,
    CompanyView,
    delete_object,
    visa_set_done,
)

app_name = "agency"

urlpatterns = [
    path("", index, name="index"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("company/", CompanyView.as_view(), name="company"),
    path("visa/", VisaView.as_view(), name="visa"),
    path("visa/<int:done>/", VisaView.as_view, name="visa"),
    path("ticket/", TicketView.as_view(), name="ticket"),
    path("visa/done/<int:pk>/", visa_set_done, name="visa-done"),
    path("renew/", RenewView.as_view(), name="renew"),
    path("transaction/", TransactionView.as_view(), name="transaction"),
    path("delete/<str:obj>/<int:pk>/", delete_object, name="delete"),
]
