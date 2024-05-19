from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from subscription.models import PAKET, PODCAST, SONG, USER_PLAYLIST

def search(request):
    query = request.GET.get('q')  # Get the search query from the URL
    results = []
    if query:
        # Search across SONG, PODCAST, and USER_PLAYLIST
        songs = SONG.objects.filter(
            Q(id_konten__judul__icontains=query) |  # Search in SONG titles
            Q(id_artist__email_akun__username__icontains=query)  # Search in Artist usernames
        ).select_related('id_konten', 'id_artist', 'id_artist__email_akun')

        podcasts = PODCAST.objects.filter(
            Q(id_konten__judul__icontains=query) |  # Search in PODCAST titles
            Q(email_podcaster__username__icontains=query)  # Search in Podcaster usernames
        ).select_related('id_konten', 'email_podcaster', 'email_podcaster__email')

        user_playlists = USER_PLAYLIST.objects.filter(
            Q(judul__icontains=query) |  # Search in Playlist titles
            Q(email_pembuat__username__icontains=query)  # Search in Creator usernames
        ).select_related('email_pembuat', 'email_pembuat__username')

        results = list(songs) + list(podcasts) + list(user_playlists)

    context = {
        'query': query,  # Pass the query to the template
        'results': results
    }
    return render(request, 'search/search_results.html', context)
