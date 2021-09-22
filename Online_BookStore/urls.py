from django.contrib import admin
from django.urls import path
from Online_BookStore import views

urlpatterns = [
    path("", views.index, name="home"),
    path("usersignup/", views.userSignUp, name="userSignUp"),
    path("userlogin/", views.userLogin, name="userLogin"),
    path("userlogout/", views.userLogout, name="userLogout"),
    path("search/", views.search, name="search"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("category/<slug:category>", views.category, name="category"),
    path("old/", views.old, name="old"),
    path("sellbooks/", views.sellbooks, name="sellbooks"),
    path("detailedview/<int:bookid>", views.detailedview, name="detailedview"),
    path("checkout/<int:bookid>", views.checkout, name="checkout"),
    path("checkoutform/<int:bookid>", views.checkoutform, name="checkoutform"),
    path("tracker/", views.tracker, name="tracker"),
]
