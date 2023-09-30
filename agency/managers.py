from django.db import models


class TransactionManager(models.Manager):
    def get_incomes(self):
        return self.filter(is_income=True)

    def get_outcomes(self):
        return self.filter(is_income=False)


class VisaManager(models.Manager):
    def get_all_incomes(self) -> int:
        incomes = 0
        for i in self.all():
            incomes += i.get_income()
        return incomes

    def get_done(self):
        return self.filter(done=False)

    def get_not_done(self):
        return self.filter(done=True)


class TicketManager(models.Manager):
    def get_all_incomes(self) -> int:
        incomes = 0
        for i in self.all():
            incomes += i.get_income()
        return incomes


class RenewManager(models.Manager):
    def get_all_incomes(self) -> int:
        incomes = 0
        for i in self.all():
            incomes += i.get_income()
        return incomes
