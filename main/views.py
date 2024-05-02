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

def add_playlist(request):
    context = {}
    return render(request, "add_playlist.html", context)

def add_song_playlist(request):
    context = {}
    return render(request, "add_song_playlist.html", context)

def add_song(request):
    context = {}
    return render(request, "add_song.html", context)

def new_userplaylist(request):
    context = {}
    return render(request, "new_userplaylist.html", context)

def playlistform(request):
    context = {}
    return render(request, "playlist_form.html", context)

def user_playlist_details(request):
    context = {}
    return render(request, "user_playlist_details.html", context)

def user_playlistDetails(request):
    context = {}
    return render(request, "user_playlistDetails.html", context)

def play_song(request):
    context = {}
    return render(request, "play_song.html", context)
