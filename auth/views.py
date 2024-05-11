from django.shortcuts import render

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
