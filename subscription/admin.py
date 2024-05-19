from django.contrib import admin
from .models import *

# Add this:
from django.contrib.auth.admin import UserAdmin

# Now register your custom Akun model
admin.site.register(Akun, UserAdmin)

admin.site.register(PAKET)
admin.site.register(TRANSACTION)
admin.site.register(PREMIUM)
admin.site.register(Role)
admin.site.register(USER_PLAYLIST)
admin.site.register(SONG)
admin.site.register(ARTIST)
admin.site.register(KONTEN)
admin.site.register(GENRE)
admin.site.register(PODCASTER)
admin.site.register(PODCAST)
admin.site.register(EPISODE)
admin.site.register(ALBUM)
admin.site.register(LABEL)
admin.site.register(PLAYLIST)
admin.site.register(CHART)
admin.site.register(PEMILIK_HAK_CIPTA)
admin.site.register(ROYALTI)
admin.site.register(AKUN_PLAY_USER_PLAYLIST)
admin.site.register(AKUN_PLAY_SONG)
admin.site.register(PLAYLIST_SONG)
admin.site.register(DOWNLOADED_SONG)