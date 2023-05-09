from uuid import uuid4
from django.db import models

# Create your models here.


class Debt(models.Model):
    # debt_taker = models.ForeignKey()
    debt_taker = models.ForeignKey(
        "DebtTaker",
        blank=True,
        related_name="debt_taker",
        on_delete=models.CASCADE,
        null=True,
    )
    # models.ManyToOneRel
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=False)
    moneyChain_first_index = models.OneToOneField(
        "MoneyChain",
        on_delete=models.CASCADE,
        null=False,
        related_name="first_index",
    )
    moneyChain_last_index = models.OneToOneField(
        "MoneyChain",
        on_delete=models.CASCADE,
        null=False,
        related_name="last_index",
    )

    ID = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        output = f""" Title: {self.title}\n
                    Amount: {self.amount}\n
                    ID: {self.ID}\n
        """
        return output


class MoneyChain(models.Model):
    previous = models.OneToOneField(
        "MoneyChain", on_delete=models.CASCADE, null=True, related_name="previous_chain"
    )
    next = models.OneToOneField(
        "MoneyChain", on_delete=models.CASCADE, null=True, related_name="next_chain"
    )
    value = models.FloatField(blank=False, null=True)
    positive = models.BooleanField(default=True)

    #
    ID = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Value: {self.value}\n ID: {self.ID}"

    def get_chain_str(self):
        output = ""
        while self.next != None:
            if self.positive:
                output += "+" + str(self.value) + "  ==>  "
            else:
                output += "-" + str(self.value) + "  ==>  "

            self = self.next
        if self.positive:
            output += "+" + str(self.value) + "  ==>  "
        else:
            output += "-" + str(self.value) + "  ==>  "
        return output

    def set_of_security_checks(self):
        pass


class DebtTaker(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    telephone = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField(max_length=120, blank=True, null=True)
    telegram_username = models.CharField(max_length=120, blank=True, null=True)
    passport_series = models.CharField(max_length=120, blank=True, null=True)
    debts = models.ManyToManyField(Debt, blank=True, related_name="debt")

    # ID
    ID = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
