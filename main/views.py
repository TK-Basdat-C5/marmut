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

def podcast(request):
    context = {}
    return render(request, "podcast.html", context)

def daftar_chart(request):
    context = {}
    return render(request, "chart_list.html", context)

def create_episode(request):
    context = {}
    return render(request, "create_episode.html", context)

def create_podcast(request):
    context = {}
    return render(request, "create_podcast.html", context)

def create_podcast(request):
    context = {}
    return render(request, "create_podcast.html", context)

def daftar_podcast(request):
    context = {}
    return render(request, "list_podcast.html", context)

def daftar_episode(request):
    context = {}
    return render(request, "daftar_episode.html", context)

def detail_chart(request):
    context = {}
    return render(request, "chart_detail.html", context)
