import uuid
from django.db import models

# Create your models here.


class Journal(models.Model):
    date = models.DateField(unique=True)
    operations = models.ManyToManyField("Operation", related_name="operations")
    shift_is_closed = models.BooleanField(default=False)

    cash_left = models.FloatField(default=0)
    terminal_income = models.FloatField(default=0)

    def __str__(self):
        return str(self.date) + " " + str(self.get_total())

    def get_total(self):
        total = 0
        for operation in self.operations.all():
            total += operation.amount
        total += self.cash_left
        total += self.terminal_income

        return total

    def close_shift(self):
        self.shift_is_closed = True
        self.save()

    def get_operations(self):
        return self.operations.all()

    def get_list_of_operations(self):
        operations = []
        for operation in self.operations.all():
            operations.append(operation)
        return operations

    def get_all_operations(self):
        operations = []
        for operation in self.operations.all():
            operations.append(
                {
                    "information": operation.information,
                    "operation_type": operation.operation_type,
                    "time": operation.time,
                    "amount": operation.amount,
                    "ID": operation.ID,
                }
            )
        return operations

    def remove_operation(self, operation):
        self.operations.remove(operation)
        self.save()

    def add_operation(self, operation):
        self.operations.add(operation)
        self.save()


class Operation(models.Model):
    operation_types = {
        ("CASH", "CASH"),
        ("CARD", "CARD"),
        ("TRANSFER", "TRANSFER"),
    }

    ID = models.UUIDField(
        primary_key=True, editable=False, unique=True, default=uuid.uuid4
    )
    journal = models.ForeignKey(
        Journal, on_delete=models.CASCADE, related_name="journal_operations", null=True
    )
    information = models.CharField(max_length=1000)
    operation_type = models.CharField(max_length=100, choices=operation_types)
    time = models.TimeField(auto_now_add=True)
    amount = models.FloatField()

    def __str__(self):
        return (
            self.information
            + " = $"
            + str(self.amount)
            + " on "
            + str(self.time)
            + "\n"
            + str(self.ID)
        )
