from django.contrib.auth.decorators import login_required
from datetime import timezone
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import  Akun, USER_PLAYLIST,  SONG, ARTIST, KONTEN, PODCAST, PODCASTER, ALBUM, LABEL
from subscription.models import PAKET
from .models import  Akun, PAKET, TRANSACTION, PREMIUM, USER_PLAYLIST,  SONG, ARTIST, KONTEN, PODCAST, PODCASTER, ALBUM, LABEL


@login_required 
def subscription_list(request):
    user = request.user
    if user.premium_user:
        messages.error(request, 'Anda sudah berlangganan paket premium')
        return redirect('dashboard')

    paket_list = PAKET.objects.all()
    context = {'paket_list': paket_list, 'is_premium': user.premium_user}
    return render(request, 'subscription/subscription_list.html', context)


@login_required
def payment(request, paket_jenis):
    user = request.user
    paket = PAKET.objects.get(jenis=paket_jenis)

    if user.premium_user:
        messages.error(request, 'Anda sudah berlangganan paket premium')
        return redirect('dashboard')

    if request.method == 'POST':
        # Process payment details (replace with actual integration)
        # ... Your payment gateway integration logic ...

        # Create a TRANSACTION record
        transaction = TRANSACTION.objects.create(
            email=user,
            jenis_paket=paket,
            timestamp_dimulai=timezone.now(),
            timestamp_berakhir=timezone.now() + timezone.timedelta(days=30),  # 1 month subscription
            metode_bayar=request.POST.get('metode_bayar'),
            nominal=paket.harga
        )

        # Add user to Premium table
        premium_user, created = PREMIUM.objects.get_or_create(email=user)

        # Update user's premium status
        user.premium_user = True
        user.save()

        messages.success(request, 'Berlangganan berhasil! Anda sekarang adalah pengguna premium')
        return redirect('dashboard') 

    context = {
        'paket': paket,  # The chosen package for the subscription
        'payment_methods': ['Transfer Bank', 'Kartu Kredit', 'E-Wallet']  # Example payment methods
    }
    return render(request, 'subscription/payment.html', context)

@login_required
def transaction_history(request):
    user = request.user
    transactions = TRANSACTION.objects.filter(email=user).order_by('-timestamp_dimulai')
    context = {'transactions': transactions}
    return render(request, 'subscription/transaction_history.html', context)