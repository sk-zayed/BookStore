from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, authenticate, login, logout
from .models import Customer, Book, Contact, Order, OrderUpdate, SoldBook
from django.urls import reverse
import json, datetime

# Create your views here.
def index(request):
    return render(request, "index.html")


def userSignUp(request):
    if request.method == "POST":
        next = request.POST.get('next', '')
        signupusername = request.POST.get("signupusername", "")
        firstname = request.POST.get("firstname", "")
        lastname = request.POST.get("lastname", "")
        email = request.POST.get("email", "")
        pass1 = request.POST.get("signuppass1", "")
        pass2 = request.POST.get("signuppass2", "")

        if len(signupusername) > 10:
           messages.error(request, "Username must be under 10 character.")
           return redirect(next) 

        if not signupusername.isalnum():
            messages.error(request, "Username cannot contain special character.")
            return redirect(next)

        if pass1 != pass2:
            messages.error(request, "Password did not match.")
            return redirect(next)

        myuser = User.objects.create_user(signupusername, email, pass1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        messages.success(request, "Your BookStore accout has been successfully created.")
        return redirect(next)


def userLogin(request):
    if request.method == "POST":
        next = request.POST.get('next', '')
        loginusername = request.POST.get("loginusername", "")
        loginpass = request.POST.get("loginpass", "")

        user = authenticate(username=loginusername, password=loginpass)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect(next)

        else:
            messages.error(request, "Invalid username or password.")
            return redirect(next)


def userLogout(request):
    logout(request)
    messages.success(request, "Loggedout successfully.")
    return redirect("home")


def search(request):
    query = request.GET.get("query", "")

    if len(query) > 25 or not query or query.isspace():
        booklist = Book.objects.none()

    else:
        booklist = Book.objects.filter(book_name__icontains=query)
        
    param = {"book": booklist, "query": query, "title": "Search results"}
    return render(request, "listview.html", param)


def about(request):
    return render(request, "about.html")


def contact(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname", "")
        lastname = request.POST.get("lastname", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        desc = request.POST.get("desc", "")
        contact = Contact(firstname=firstname, lastname=lastname,
                          email=email, phone=phone, desc=desc)
        contact.save()
        messages.success(request, "Thank you for contacting us. Your query would be reviewed by our team soon.")

    return render(request, "contact.html")


def category(request, category):
    booklist = []
    books = Book.objects.filter(category=category)

    for book in books:
        booklist.append(book)

    param = {"book": booklist, "title": category}
    return render(request, "listview.html", param)


def old(request):
    old = []
    books = Book.objects.filter(category="Old")

    for book in books:
        old.append(book)

    param = {"book": old, "title": "Old"}
    return render(request, "listview.html", param)


def sellbooks(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname", "")
        lastname = request.POST.get("lastname", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        address = request.POST.get("address", "")
        city = request.POST.get("city", "")
        state = request.POST.get("state", "")
        zipcode = request.POST.get("zipcode", "")
        bookname = request.POST.get("bookname", "")
        category = request.POST.get("category", "")

        customer = Customer.objects.filter(firstname=firstname, lastname=lastname, email=email, phone=phone, address=address, city=city, state=state, zipcode=zipcode)

        if customer.exists():
            soldbook = SoldBook(book_name=bookname, category=category, customer=customer[0])
            
        else:
            customer = Customer(firstname=firstname, lastname=lastname, email=email, phone=phone, address=address, city=city, state=state, zipcode=zipcode)
            customer.save()

            soldbook = SoldBook(book_name=bookname, category=category)

        soldbook.save()

        messages.success(request, "Thank you for selling a book. We will let you know the price of book soon.")

    return render(request, "sellbooks.html")


def detailedview(request, bookid):
    book = Book.objects.filter(book_id=bookid)
    return render(request, "detailedview.html", {"book": book[0]})


def checkout(request, bookid):
    book = Book.objects.filter(book_id=bookid)
    return render(request, "checkout.html", {"book": book[0]})


def checkoutform(request, bookid):
    if request.method == "POST":
        firstname = request.POST.get("firstname", "")
        lastname = request.POST.get("lastname", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        address = request.POST.get("address", "")
        city = request.POST.get("city", "")
        state = request.POST.get("state", "")
        zipcode = request.POST.get("zipcode", "")
        book = Book.objects.filter(book_id=bookid)
        bookname = book[0].book_name
        bookcat = book[0].category
        bookcost = book[0].price + 50

        customer = Customer.objects.filter(firstname=firstname, lastname=lastname, email=email, phone=phone, address=address, city=city, state=state, zipcode=zipcode)

        if customer.exists():
            order = Order(ordered_book=bookname, book_category=bookcat, book_cost=bookcost, customer=customer[0])
            
        else:
            customer = Customer(firstname=firstname, lastname=lastname, email=email, phone=phone, address=address, city=city, state=state, zipcode=zipcode)
            customer.save()

            order = Order(ordered_book=bookname, book_category=bookcat, book_cost=bookcost, customer=customer)

        order.save()

        update = OrderUpdate(order_id=order.order_id,
                             update_desc="The order has been placed.", timestamp=str(datetime.datetime.now())[:-7])
        update.save()

        messages.success(request, f"Thank you for ordering {bookname}. Your tracker id for the order is {order.order_id}.")

    return redirect(reverse("home"))


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get("orderId", "")
        email = request.POST.get("trackemail", "")
        updates = []

        try:
            cemail = Customer.objects.filter(order__order_id=orderId)[0].email

            if cemail==email:
                update = OrderUpdate.objects.filter(order_id=orderId)

                for item in update:
                    updates.append(
                        {'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(updates, default=str)
                return HttpResponse(response)

            else:
                response = json.dumps(updates, default=str)
                return HttpResponse(response)
                
        except:
            response = json.dumps(updates, default=str)
            return HttpResponse(response)

    return render(request, "tracker.html")