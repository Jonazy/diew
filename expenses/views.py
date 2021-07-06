from django.shortcuts import render, redirect
from .models import Expense, Category
from django.contrib import messages
# Create your views here.


def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    context = {
        "categories": categories,
        "expenses": expenses
    }
    return render(request, 'expenses/index.html', context)


def addExpense(request):
    categories = Category.objects.all()

    context = {
        "categories": categories,
    }
    if request.method == "GET":
        return render(request, 'expenses/add_expense.html', context)

    if request.method == "POST":
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['date']
        if not amount:
            messages.error(request, "Please enter amount")
        if not description:
            messages.error(request, "Please enter description")
        if not category:
            messages.error(request, "Please enter category")
        if not date:
            messages.error(request, "Please enter date")
        Expense.objects.create(owner=request.user, amount=amount, description=description,
                               category=category, date=date)
        messages.success(request, "Expense saved successfully")
        context = {
            "categories": categories,
            "values": request.POST
        }
        return render(request, 'expenses/add_expense.html', context)


def editExpense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()

    context = {
        "categories": categories,
        "expense": expense,
        "values": expense,
    }
    if request.method == "GET":
        return render(request, 'expenses/edit_expense.html', context)

    if request.method == "POST":
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['date']
        if not amount:
            messages.error(request, "Please enter amount")
            return render(request, 'expenses/edit_expense.html', context)
        if not description:
            messages.error(request, "Please enter description")
            return render(request, 'expenses/edit_expense.html', context)
        if not category:
            messages.error(request, "Please enter category")
            return render(request, 'expenses/edit_expense.html', context)
        if not date:
            messages.error(request, "Please enter date")
            return render(request, 'expenses/edit_expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense.description = description
        expense.category = category
        expense.date = date
        expense.save()
        messages.success(request, "Expense updated successfully")

        return redirect('index')


def deleteExpense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    expense.delete()
    messages.error(request, "Expense deleted successfully")
    return redirect('index')