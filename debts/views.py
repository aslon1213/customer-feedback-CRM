from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.admin.views.decorators import staff_member_required

# import messages
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import Debt, MoneyChain, DebtTaker
from django import http

# Create your views here.


@login_required(login_url="account_login")
@staff_member_required(login_url="account_login")
def list_debts(request):
    debts = Debt.objects.all()
    ds = {}
    histories = []
    for debt in debts:
        chain = debt.moneyChain_first_index
        history = MoneyChain.objects.get(ID=chain.ID).get_chain_str()
        histories.append(history)
    print(histories)
    return render(
        request=request,
        template_name="debts/list_all.html",
        context={"debts": debts, "histories": histories},
    )


@login_required(login_url="account_login")
def create_debt(request):
    if not request.user.is_staff:
        messages.error(
            "Unauthorized access!!!! You are not Allowed to access this page"
        )
        return redirect("main_page")

    if request.method == "POST":
        print(request.POST)
        print("POST")
        amount = request.POST["amount"]
        title = request.POST["title"]
        description = request.POST["description"]
        debt_taker = DebtTaker.objects.create(
            first_name="Someone",
        )
        debt_taker.save
        chain = MoneyChain.objects.create(
            previous=None,
            next=None,
            value=float(amount),
            positive=False,
        )
        chain_obj = chain.save
        obj = Debt.objects.create(
            amount=float(amount),
            title=title,
            description=description,
            moneyChain_first_index=chain,
            moneyChain_last_index=chain,
            debt_taker=debt_taker,
        )
        obj.save
        return redirect("list-debts")
    elif request.method == "GET":
        return render(request, "debts/create_debt.html")
    else:
        # http response bad request
        return http.HttpResponseBadRequest()


@login_required(login_url="account_login")
def transaction_plus(request, pk):
    if not request.user.is_staff:
        messages.error(
            "Unauthorized access!!!! You are not Allowed to access this page"
        )
        return redirect("main_page")
    if request.method == "POST":
        debt = Debt.objects.get(ID=pk)
        chain = debt.moneyChain_last_index
        value = request.POST["value"]
        if float(value) < 0:
            messages.error("Wrong path, go transaction plus")
            return redirect(list_debts)

        chain_object = MoneyChain.objects.get(ID=chain.ID)
        next_chain = MoneyChain.objects.create(
            value=float(value),
            previous=chain,
            positive=False,
        )
        next_chain.save()
        chain_object.next = next_chain
        chain_object.save()
        print("Prev: ", debt.amount)
        debt.amount += float(value)
        debt.moneyChain_last_index = next_chain
        print("Next", debt.amount)
        debt.save()
        return redirect("list-debts")
    elif request.method == "GET":
        context = {"debt": Debt.objects.get(ID=pk), "status": "plus"}
        return render(request, "debts/transaction.html", context=context)
    else:
        # http response bad request
        return http.HttpResponseBadRequest()


@login_required(login_url="account_login")
def transaction_minus(request, pk):
    if not request.user.is_staff:
        messages.error(
            "Unauthorized access!!!! You are not Allowed to access this page"
        )
        return redirect("main_page")
    if request.method == "POST":
        debt = Debt.objects.get(ID=pk)
        chain = debt.moneyChain_last_index
        value = request.POST["value"]
        if float(value) < 0:
            messages.error("Wrong path, go transaction plus")
            return redirect(list_debts)

        chain_object = MoneyChain.objects.get(ID=chain.ID)
        next_chain = MoneyChain.objects.create(
            value=float(value),
            previous=chain,
            positive=True,
        )
        next_chain.save()
        chain_object.next = next_chain
        chain_object.save()
        print("Prev: ", debt.amount)
        debt.amount -= float(value)
        debt.moneyChain_last_index = next_chain
        print("Next", debt.amount)
        debt.save()
        return redirect("list-debts")
    elif request.method == "GET":
        context = {"debt": Debt.objects.get(ID=pk), "status": "minus"}
        return render(request, "debts/transaction.html", context=context)
    else:
        # http response bad request
        return http.HttpResponseBadRequest()


@login_required(login_url="account_login")
def delete_debt(request, pk):
    print("METHOD: ", request.method)
    if not request.user.is_staff:
        messages.error(
            "Unauthorized access!!!! You are not Allowed to access this page"
        )
        return redirect("main_page")
    if request.method == "POST":
        print("POST")
        password = request.POST["password"]
        word = request.POST["word"]
        if word != "delete":
            messages.error(request, "Wrong word")
            return redirect("list-debts")
        user = request.user
        if not check_password(password, user.password):
            messages.error(request, "Wrong password")
            return redirect("list-debts")

        debt = Debt.objects.get(ID=pk)
        debt.delete()
        return redirect("list-debts")
    elif request.method == "GET":
        context = {"debt": Debt.objects.get(ID=pk)}

        # generate some two words for confirmation
        words = [
            "delete",
            "remove",
            "erase",
            "destroy",
            "obliterate",
            "annihilate",
            "extinguish",
            "extirpate",
        ]

        return render(request, "debts/delete_debt.html", context=context)
    else:
        # http response bad request
        return http.HttpResponseBadRequest()


@login_required(login_url="account_login")
@staff_member_required(login_url="main_page")
def get_debt_history(request, pk):
    debt = Debt.objects.get(ID=pk)
    chain = debt.moneyChain_first_index
    chain = MoneyChain.objects.get(ID=chain.ID)
    histories = []
    while chain.next != None:
        chain = chain.next
        histories.append(chain)

    return render(
        request=request,
        template_name="debts/debt_history.html",
        context={"histories": histories, "debt": debt},
    )


@staff_member_required(login_url="main_page")
def debt_taker_page(request, pk):
    debt_taker = DebtTaker.objects.get(ID=pk)
    debts = Debt.objects.filter(debt_taker_id=pk)
    context = {"debt_taker": debt_taker, "debts": debts}
    return render(request, "debts/debt_taker_page.html", context=context)
