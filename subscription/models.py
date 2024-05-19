import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Akun(AbstractUser):
    # ... (Existing fields from AbstractUser) ...
    gender = models.IntegerField(default=0)  # 0 for female, 1 for male
    tempat_lahir = models.CharField(max_length=50)
    tanggal_lahir = models.DateField()
    is_verified = models.BooleanField(default=False)
    kota_asal = models.CharField(max_length=50)
    premium_user = models.BooleanField(default=False)
    role = models.ManyToManyField('Role', blank=True)  # Many-to-many relationship with Role

    # Add 'related_name' to 'groups' and 'user_permissions' fields:
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='custom_user_set',  #  New related_name here
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',  #  New related_name here
    )

class Role(models.Model):
    role = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.role


class PAKET(models.Model):
    jenis = models.CharField(max_length=50, primary_key=True)
    harga = models.IntegerField()

    def __str__(self):
        return self.jenis

class TRANSACTION(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jenis_paket = models.ForeignKey(PAKET, on_delete=models.CASCADE)
    email = models.ForeignKey(Akun, on_delete=models.CASCADE)
    timestamp_dimulai = models.DateTimeField(default=timezone.now)
    timestamp_berakhir = models.DateTimeField(blank=True, null=True)
    metode_bayar = models.CharField(max_length=50)
    nominal = models.IntegerField()

    def __str__(self):
        return f"{self.jenis_paket} - {self.email} - {self.timestamp_dimulai}"

class PREMIUM(models.Model):
    email = models.OneToOneField(Akun, on_delete=models.CASCADE, primary_key=True)  # Change to OneToOneField

    def __str__(self):
        return self.email

class USER_PLAYLIST(models.Model):
    email_pembuat = models.ForeignKey(Akun, on_delete=models.CASCADE)
    id_user_playlist = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    judul = models.CharField(max_length=100)
    deskripsi = models.TextField()
    jumlah_lagu = models.IntegerField(default=0)
    tanggal_dibuat = models.DateField(default=timezone.now)
    id_playlist = models.ForeignKey('PLAYLIST', on_delete=models.CASCADE)
    total_durasi = models.IntegerField(default=0)

    def __str__(self):
        return self.judul

class SONG(models.Model):
    id_konten = models.OneToOneField('KONTEN', on_delete=models.CASCADE, primary_key=True)
    id_artist = models.ForeignKey('ARTIST', on_delete=models.CASCADE)
    id_album = models.ForeignKey('ALBUM', on_delete=models.CASCADE, null=True, blank=True)
    total_play = models.IntegerField(default=0)
    total_download = models.IntegerField(default=0)

    def __str__(self):
        return self.id_konten.judul

class ARTIST(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email_akun = models.ForeignKey(Akun, on_delete=models.CASCADE)
    id_pemilik_hak_cipta = models.ForeignKey('PEMILIK_HAK_CIPTA', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.email_akun.username} - {self.id_pemilik_hak_cipta}"

class KONTEN(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    judul = models.CharField(max_length=100)
    tanggal_rilis = models.DateField(default=timezone.now)
    tahun = models.IntegerField()
    durasi = models.IntegerField()
    genre = models.ManyToManyField('GENRE', blank=True)

    def __str__(self):
        return self.judul

class GENRE(models.Model):
    genre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.genre

class PODCASTER(models.Model):
    email = models.OneToOneField(Akun, on_delete=models.CASCADE, primary_key=True)  # Change to OneToOneField

    def __str__(self):
        return self.email

class PODCAST(models.Model):
    id_konten = models.OneToOneField('KONTEN', on_delete=models.CASCADE, primary_key=True)
    email_podcaster = models.ForeignKey('PODCASTER', on_delete=models.CASCADE)

    def __str__(self):
        return self.id_konten.judul

class EPISODE(models.Model):
    id_episode = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_konten_podcast = models.ForeignKey('PODCAST', on_delete=models.CASCADE)
    judul = models.CharField(max_length=100)
    deskripsi = models.TextField()
    durasi = models.IntegerField()
    tanggal_rilis = models.DateField(default=timezone.now)

    def __str__(self):
        return self.judul

class ALBUM(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    judul = models.CharField(max_length=100)
    jumlah_lagu = models.IntegerField(default=0)
    id_label = models.ForeignKey('LABEL', on_delete=models.CASCADE)
    total_durasi = models.IntegerField(default=0)

    def __str__(self):
        return self.judul

class LABEL(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=100)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    kontak = models.CharField(max_length=50)
    id_pemilik_hak_cipta = models.ForeignKey('PEMILIK_HAK_CIPTA', on_delete=models.CASCADE)

    def __str__(self):
        return self.nama

class PLAYLIST(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"Playlist {self.id}"

class CHART(models.Model):
    tipe = models.CharField(max_length=50, primary_key=True)
    id_playlist = models.ForeignKey('PLAYLIST', on_delete=models.CASCADE)

    def __str__(self):
        return self.tipe

class PEMILIK_HAK_CIPTA(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rate_royalti = models.IntegerField()

    def __str__(self):
        return f"Pemilik Hak Cipta {self.id}"

class ROYALTI(models.Model):
    id_pemilik_hak_cipta = models.ForeignKey('PEMILIK_HAK_CIPTA', on_delete=models.CASCADE)
    id_song = models.ForeignKey('SONG', on_delete=models.CASCADE)
    jumlah = models.IntegerField()

    def __str__(self):
        return f"{self.id_pemilik_hak_cipta} - {self.id_song}"

class AKUN_PLAY_USER_PLAYLIST(models.Model):
    email_pemain = models.ForeignKey(Akun, on_delete=models.CASCADE)
    id_user_playlist = models.ForeignKey('USER_PLAYLIST', on_delete=models.CASCADE)
    waktu = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('email_pemain', 'id_user_playlist', 'waktu')

    def __str__(self):
        return f"{self.email_pemain} - {self.id_user_playlist} - {self.waktu}"

class AKUN_PLAY_SONG(models.Model):
    email_pemain = models.ForeignKey(Akun, on_delete=models.CASCADE)
    id_song = models.ForeignKey('SONG', on_delete=models.CASCADE)
    waktu = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('email_pemain', 'id_song', 'waktu')

    def __str__(self):
        return f"{self.email_pemain} - {self.id_song} - {self.waktu}"

class PLAYLIST_SONG(models.Model):
    id_playlist = models.ForeignKey('PLAYLIST', on_delete=models.CASCADE)
    id_song = models.ForeignKey('SONG', on_delete=models.CASCADE)
    durasi = models.IntegerField()

    class Meta:
        unique_together = ('id_playlist', 'id_song')

    def __str__(self):
        return f"{self.id_playlist} - {self.id_song}"

class DOWNLOADED_SONG(models.Model):
    id_song = models.ForeignKey('SONG', on_delete=models.CASCADE)
    email_downloader = models.ForeignKey(Akun, on_delete=models.CASCADE)
    timestamp_dimulai = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('id_song', 'email_downloader')

    def __str__(self):
        return f"{self.id_song} - {self.email_downloader}"