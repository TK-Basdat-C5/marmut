from django.shortcuts import render

def landing(request):
    context = {}
    return render(request, "landing.html", context)

def login(request):
    context = {}
    return render(request, "login.html", context)

def register(request):
    context = {}
    return render(request, "register.html", context)

def register_label(request):
    context = {}
    return render(request, "register_label.html", context)

def register_pengguna(request):
    context = {}
    return render(request, "register_pengguna.html", context)

def dashboard(request):
    context = {}
    return render(request, "dashboard.html", context)
