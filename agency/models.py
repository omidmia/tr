from django.db import models
from django.utils.timezone import now
from .managers import TransactionManager, VisaManager, TicketManager, RenewManager


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=300, unique=False)
    phone = models.BigIntegerField(null=True, default=None)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    date = models.DateTimeField(default=now)
    value = models.IntegerField()
    is_income = models.BooleanField(default=False)
    description = models.CharField(max_length=300, null=True, default=None)

    objects = TransactionManager()


class Ticket(models.Model):
    ticket_type = models.CharField(
        max_length=1, choices=[("a", "By Air"), ("e", "by Earth")], default="e"
    )
    customer_name = models.CharField(max_length=300)
    phone = models.CharField(max_length=13)
    passport_number = models.BigIntegerField()
    real_price = models.IntegerField(default=1600)
    price = models.IntegerField()
    spended = models.IntegerField()
    description = models.CharField(max_length=800, null=True, default=None)
    from_city = models.CharField(max_length=200, null=True, default="")
    to_city = models.CharField(max_length=200, null=True, default="")
    do_date = models.DateField()

    objects = TicketManager()

    def get_income(self: object) -> int:
        return self.price - self.real_price - self.spended


class Visa(models.Model):
    VIASTERMCHOICES = [
        ("2", "Two month"),
        ("3", "Three month"),
        ("4", "45 days"),
    ]
    customer_name = models.CharField(max_length=300)
    phone = models.CharField(max_length=13)
    passport_number = models.BigIntegerField()
    visa_term = models.CharField(max_length=1, choices=VIASTERMCHOICES, default="2")
    real_price = models.IntegerField(default=1600)
    price = models.IntegerField()
    spended = models.IntegerField()
    description = models.CharField(max_length=800, null=True, default=None)
    city = models.CharField(max_length=200, null=True, default="")
    do_date = models.DateField()
    functor = models.ForeignKey(
        to=Company, related_name="visas", on_delete=models.PROTECT
    )
    done = models.BooleanField(default=False)
    objects = VisaManager()

    def get_income(self: object) -> int:
        return self.price - self.real_price - self.spended


class Renew(models.Model):
    type_choices = [
        ("e", "Exit"),
        ("r", "Renew"),
    ]
    customer_name = models.CharField(max_length=300)
    phone = models.CharField(max_length=13)
    passport_number = models.BigIntegerField()
    renew_type = models.CharField(max_length=1, choices=type_choices, default="2")
    real_price = models.IntegerField(default=1600)
    price = models.IntegerField()
    spended = models.IntegerField()
    description = models.CharField(max_length=800, null=True, default=None)
    city = models.CharField(max_length=200, null=True, default="")
    do_date = models.DateField()
    functor = models.ForeignKey(
        to=Company, related_name="renews", on_delete=models.PROTECT
    )

    objects = RenewManager()

    def get_income(self: object) -> int:
        return self.price - self.real_price - self.spended
