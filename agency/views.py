from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render, reverse, get_object_or_404
from django.http.response import HttpResponseNotFound
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from .models import Company, Ticket, Transaction, Visa, Renew

# Create your views here.


@login_required
def index(request):
    visa_incomes = Visa.objects.get_all_incomes()
    renew_incomes = Renew.objects.get_all_incomes()
    ticket_incomes = Ticket.objects.get_all_incomes()
    all_incomes = visa_incomes + renew_incomes + ticket_incomes
    context = {
        "visa_incomes": visa_incomes,
        "renew_incomes": renew_incomes,
        "ticket_incomes": ticket_incomes,
        "all_incomes": all_incomes,
    }
    return render(request=request, template_name="index.html", context=context)


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = "login.html"
    redirect_authenticated_user = True


class VisaView(LoginRequiredMixin, View):
    def get(self, request, done=0):
        if done == 1:
            visas = Visa.objects.get_done()[::-1]
        else:
            visas = Visa.objects.get_not_done()[::-1]

        incomes = Visa.objects.get_all_incomes()
        functors = Company.objects.all()
        context = {"visas": visas, "functors": functors, "incomes": incomes}
        return render(request=request, template_name="visa.html", context=context)

    def post(self, request):
        error = ""
        customer_name = request.POST.get("customer_name")
        phone = request.POST.get("phone")
        passport_number = request.POST.get("passport_number")
        visa_term = request.POST.get("visa_term")
        price = request.POST.get("price")
        real_price = request.POST.get("real_price")
        city = request.POST.get("city")
        functor = Company.objects.get(name=request.POST.get("functor"))
        spended = request.POST.get("spended")
        do_date = request.POST.get("do_date")
        description = request.POST.get("description")
        try:
            visa = Visa.objects.create(
                customer_name=customer_name,
                phone=phone,
                description=description,
                visa_term=visa_term,
                price=price,
                real_price=real_price,
                city=city,
                functor=functor,
                spended=spended,
                do_date=do_date,
                passport_number=passport_number,
            )
            visa.save()
            Transaction.objects.create(
                value=visa.spended, description=f"for {visa.customer_name} visa"
            )
            return redirect(reverse("agency:visa"))
        except Exception as e:
            error = e
        finally:
            visas = Visa.objects.all()[::-1]
            functors = Company.objects.all()
            context = {"visas": visas, "functors": functors, "error": error}
            return render(request=request, template_name="visa.html", context=context)


class TicketView(LoginRequiredMixin, View):
    def get(self, request):
        tickets = Ticket.objects.all()[::-1]
        incmoes = Ticket.objects.get_all_incomes()
        context = {
            "tickets": tickets,
            "incomes": incmoes,
        }
        return render(request=request, template_name="ticket.html", context=context)

    def post(self, request):
        error = ""
        ticket_type = request.POST.get("ticket_type")
        customer_name = request.POST.get("customer_name")
        phone = request.POST.get("phone")
        passport_number = request.POST.get("passport_number")
        real_price = request.POST.get("real_price")
        price = request.POST.get("price")
        spended = request.POST.get("spended")
        description = request.POST.get("description")
        from_city = request.POST.get("from_city")
        to_city = request.POST.get("to_city")
        do_date = request.POST.get("do_date")
        try:
            ticket = Ticket.objects.create(
                ticket_type=ticket_type,
                customer_name=customer_name,
                phone=phone,
                passport_number=passport_number,
                real_price=real_price,
                price=price,
                spended=spended,
                description=description,
                from_city=from_city,
                to_city=to_city,
                do_date=do_date,
            )
            ticket.save()
            return redirect(reverse("agency:ticket"))
        except Exception as e:
            error = e
        finally:
            tickets = Ticket.objects.all()[::-1]
            context = {
                "tickets": tickets,
                "error": error,
            }
            return render(request=request, template_name="ticket.html", context=context)


class RenewView(LoginRequiredMixin, View):
    def get(self, request):
        error = ""
        functors = Company.objects.all()
        renews = Renew.objects.all()[::-1]
        context = {"functors": functors, "error": error, "renews": renews}
        return render(request=request, template_name="renew.html", context=context)

    def post(self, request):
        error = ""
        customer_name = request.POST.get("customer_name")
        phone = request.POST.get("phone")
        passport_number = request.POST.get("passport_number")
        renew_type = request.POST.get("renew_type")
        real_price = request.POST.get("real_price")
        price = request.POST.get("price")
        spended = request.POST.get("spended")
        description = request.POST.get("description")
        city = request.POST.get("city")
        do_date = request.POST.get("do_date")
        functor = Company.objects.get(name=request.POST.get("functor"))
        try:
            r = Renew.objects.create(
                customer_name=customer_name,
                phone=phone,
                passport_number=passport_number,
                renew_type=renew_type,
                real_price=real_price,
                price=price,
                spended=spended,
                description=description,
                city=city,
                do_date=do_date,
                functor=functor,
            )
            r.save()
            return redirect(reverse("agency:renew"))
        except Exception as e:
            error = e
        finally:
            functors = Company.objects.all()
            renews = Renew.objects.all()[::-1]
            context = {"functors": functors, "error": error, "renews": renews}
            return render(request=request, template_name="renew.html", context=context)


class CompanyView(View):
    def get(self, request):
        companies = Company.objects.all()
        return render(
            request=request,
            template_name="company.html",
            context={"companies": companies},
        )

    def post(self, request):
        name = request.POST.get("name")
        phone = request.POST.get("phone")

        Company.objects.create(name=name, phone=phone)

        return redirect(reverse("agency:company"))


class TransactionView(LoginRequiredMixin, View):
    def get(self, request):
        transactions = Transaction.objects.get_outcomes()
        e = ""
        return render(
            request=request,
            template_name="transaction.html",
            context={"error": e, "transactions": transactions},
        )

    def post(self, request):
        value = request.POST.get("value")
        description = request.POST.get("description")
        try:
            t = Transaction.objects.create(value=value, description=description)
            t.save()
            return redirect(reverse("agency:transaction"))
        except Exception as e:
            return render(
                request=request, template_name="transaction.html", context={"error": e}
            )


@login_required
def delete_object(request, obj="visa", pk=""):
    try:
        if obj == "visa":
            visa = get_object_or_404(Visa, pk=pk)
            income = visa.real_price - visa.spended - visa.price
            visa.delete()
            return redirect(reverse("agency:visa"))
        elif obj == "ticket":
            ticket = get_object_or_404(Ticket, pk=pk)
            income = ticket.real_price - ticket.spended - ticket.price
            ticket.delete()
            return redirect(reverse("agency:ticket"))
        elif obj == "transaction":
            tr = get_object_or_404(Transaction, pk=pk)
            tr.delete()
            return redirect(reverse("agency:transactions"))
        elif obj == "renew":
            renew = get_object_or_404(Renew, pk=pk)
            income = renew.real_price - renew.spended - renew.price
            renew.delete()
            return redirect(reverse("agency:renew"))
        elif obj == "company":
            compnay = get_object_or_404(Company, pk=pk)
            compnay.delete()
            return redirect(reverse("agency:company"))
    except Exception as e:
        print(e)
        return redirect(reverse("agency:index"))


@login_required
def visa_set_done(request, pk):
    visa = get_object_or_404(Visa, pk=pk)
    visa.done = True
    visa.save()
    return redirect(reverse("agency:visa"))
