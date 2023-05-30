import json
import time
from django import http
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required

from workday_finance_management.models import Journal, Operation


# rest_framework
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import JournalSerializer, OperationSerializer

# Create your views here.


class JournalWrapperWithOperations:
    def __init__(self, journal):
        self.journal = journal
        self.operations = journal.get_list_of_operations()
        self.total = journal.get_total()


def main_view(request):
    journals = Journal.objects.all().order_by("-date")
    context = {}
    js = []
    for journal in journals:
        js.append(JournalWrapperWithOperations(journal))
    context["journals"] = js
    try:
        if request.headers["format"] == "application/json":
            context = {}
        serialized_journals = []
        for journal in journals:
            serialized_journals.append(
                {
                    "date": journal.date,
                    "operations": list(journal.get_all_operations()),
                    "shift_is_closed": journal.shift_is_closed,
                    "cash_left": journal.cash_left,
                    "terminal_income": journal.terminal_income,
                    "total": journal.get_total(),
                }
            )
        context["journals"] = serialized_journals
        return JsonResponse(context)
    except KeyError:
        pass

    return render(request, "workday_finance_management/main.html", context)


def new_journal(request):
    if request.method == "POST":
        data = request.body.decode("utf-8")
        try:
            data = json.loads(data)
            date = data["date"]
            date = time.strptime(date, "%d.%m.%Y")
            date = time.strftime("%Y-%m-%d", date)

            journal = Journal.objects.create(date=date)
        except Exception as e:
            return http.HttpResponseBadRequest(
                json.dumps(
                    {
                        "status": "error",
                        "error": str(e),
                        "message": "No date provided or date is in wrong format",
                        "date": "DD-MM-YYYY",
                    }
                )
            )
        journal.save()
        return JsonResponse({"status": "ok", "journal_id": journal.id})
    else:
        return http.HttpResponseBadRequest(
            json.dumps({"status": "error", "message": "Only POST requests are allowed"})
        )


def view_journal(request):
    context = {}
    try:
        data = request.body.decode("utf-8")
        data = json.loads(data)
        date = data["date"]
        date = time.strptime(date, "%d.%m.%Y")
        date = time.strftime("%Y-%m-%d", date)
        journal = Journal.objects.filter(date=date).first()
        if journal is None:
            return http.HttpResponseBadRequest(
                json.dumps(
                    {
                        "status": "error",
                        "message": "Journal does not exist",
                        "date": data["date"],
                    }
                )
            )
        if request.headers["format"] == "application/json":
            context["journal"] = {
                "date": journal.date,
                "operations": list(journal.get_all_operations()),
                "shift_is_closed": journal.shift_is_closed,
                "cash_left": journal.cash_left,
                "terminal_income": journal.terminal_income,
                "total": journal.get_total(),
            }
            return JsonResponse(context)
    except KeyError:
        return http.HttpResponseBadRequest(
            json.dumps(
                {
                    "status": "error",
                    "error": "KEY ERROR",
                    "message": "No format provided",
                }
            )
        )

    return render(request, "workday_finance_management/view_journal.html", context)


def new_operation(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        print(data)
        date = data["date"]
        date = time.strptime(date, "%d.%m.%Y")
        date = time.strftime("%Y-%m-%d", date)
        journal = Journal.objects.filter(date=date).first()
        if journal is None:
            return http.HttpResponseBadRequest(
                json.dumps(
                    {
                        "status": "error",
                        "message": "Journal does not exist",
                        "date": data["date"],
                    }
                )
            )
        elif journal.shift_is_closed:
            return http.HttpResponseBadRequest(
                json.dumps(
                    {
                        "status": "error",
                        "message": "Shift is closed",
                        "date": data["date"],
                    }
                )
            )
        try:
            if request.headers["format"] == "application/json":
                op = data["operation"]
                operation = Operation.objects.create(
                    journal=journal,
                    information=op["information"],
                    amount=op["amount"],
                    operation_type=op["operation_type"],
                    time=op["time"],
                )
                operation.save()
                journal.add_operation(operation)
                return JsonResponse(
                    {
                        "status": "ok",
                        "operation": {
                            "information": operation.information,
                            "amount": operation.amount,
                            "operation_type": operation.operation_type,
                            "time": operation.time,
                            "journal": date,
                        },
                    }
                )
        except KeyError:
            return http.HttpResponseBadRequest(
                json.dumps(
                    {
                        "status": "error",
                        "message": "format: application/json is required",
                    }
                )
            )

    else:
        return http.HttpResponseBadRequest(
            json.dumps({"status": "error", "message": "Only POST requests are allowed"})
        )

    return redirect("view_journal")


def view_operation(request):
    if request.method == "GET":
        data = json.loads(request.body)
        operation_id = data["operation_id"]
        operation = Operation.objects.get(ID=operation_id)
        return JsonResponse(
            {
                "status": "ok",
                "operation": {
                    "information": operation.information,
                    "amount": operation.amount,
                    "operation_type": operation.operation_type,
                    "time": operation.time,
                    "journal": operation.journal.date,
                },
            }
        )
    else:
        return http.HttpResponseBadRequest(
            json.dumps(
                {"status": "error", "message": "Only DELETE requests are allowed"}
            )
        )


@api_view(["PUT"])
def edit_operation(request):
    obj = Operation.objects.get(ID=request.data["ID"])
    serializer = OperationSerializer(obj, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


def delete_operation(request):
    print("Method:", request.method)
    # return http.HttpResponseNotFound("Not found")
    if request.method == "DELETE":
        try:
            data = json.loads(request.body.decode("utf-8"))
            operation_id = data["operation_id"]
            operation = Operation.objects.get(ID=operation_id)
            if operation is None:
                return http.HttpResponseBadRequest(
                    json.dumps(
                        {
                            "status": "error",
                            "message": "Operation does not exist",
                            "operation_id": operation_id,
                        }
                    )
                )
            operation.delete()
            # journal = Journal.objects.get(id=operation.journal.id)
            # journal.remove_operation(operation)
            return JsonResponse(
                {
                    "status": "ok",
                    "operation": {
                        "information": operation.information,
                        "amount": operation.amount,
                        "operation_type": operation.operation_type,
                        "time": operation.time,
                        "journal": operation.journal.date,
                        "ID": operation.ID,
                    },
                }
            )
        except KeyError:
            return http.HttpResponseBadRequest(
                json.dumps(
                    {
                        "status": "error",
                        "message": "No operation_id provided",
                    }
                )
            )
        except Exception as e:
            return http.HttpResponseServerError(
                json.dumps(
                    {
                        "status": "error",
                        "message": str(e),
                    }
                )
            )

    else:
        return http.HttpResponseBadRequest(
            json.dumps(
                {"status": "error", "message": "Only DELETE requests are allowed"}
            )
        )


@api_view(["PUT"])
def close_current(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        cash_left = data["cash_left"]
        terminal_income = data["terminal_income"]
    except KeyError:
        return Response(
            {
                "status": "error",
                "message": "No data provided, You cannot close the journal without setting cash_left and terminal_income",
                "instuction": "Send cash_left and terminal_income",
            }
        )
    except Exception as e:
        return Response(
            {
                "status": "error",
                "message": str(e),
            }
        )
    obj = Journal.objects.all().order_by("-date").first()
    if obj.shift_is_closed:
        return Response({"status": "error", "message": "Shift is already closed"})

    obj.shift_is_closed = True
    obj.cash_left = cash_left
    obj.terminal_income = terminal_income
    obj.save()
    return Response({"status": "ok", "message": "Shift closed"})
