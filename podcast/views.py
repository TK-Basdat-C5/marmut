from datetime import date
import uuid
from django.http import HttpResponseNotFound, JsonResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from utils.query import query
from django.views.decorators.csrf import csrf_exempt

from authentication.views import check_premium, get_role_pengguna

def podcast(request, id):
    if "email" not in request.session:
        return redirect('authentication:login')
    
        
    email = request.session["email"]
    role = request.session["role"]
    roles = get_role_pengguna(email)


    query_konten = query(f"SELECT * FROM KONTEN WHERE ID = '{id}'")
    judul_podcast = query_konten[0][1]

    tanggal_rilis = query_konten[0][2]
    tanggal_rilis_formated = tanggal_rilis.strftime('%d/%m/%y')

    tahun_rilis = query_konten[0][3]
    
    total_durasi = query_konten[0][4]
    jam = total_durasi // 60
    menit = total_durasi % 60

    query_email = query(f"SELECT * FROM PODCAST WHERE ID_KONTEN = '{id}'")
    email_podcaster = query_email[0][1]

    query_nama_podcaster = query(f"SELECT nama FROM AKUN WHERE email = '{email_podcaster}'")
    nama_podcaster = query_nama_podcaster[0][0]

    query_genre = query(f"SELECT genre FROM GENRE WHERE ID_KONTEN = '{id}'")
    all_genre = []
    for i in query_genre:
        all_genre.append(i[0])

    query_episodes = query(f"SELECT judul, deskripsi, durasi, tanggal_rilis FROM episode WHERE ID_KONTEN_PODCAST = '{id}'")
    all_episodes = []

    for i in query_episodes:
        episode = []
        counter = 0
        for y in i:
            if counter == 2:
                durasi = y
                jam = durasi // 60
                menit = durasi % 60
                if jam > 0:
                    episode.append(f"{jam} jam {menit} menit")
                else:
                    episode.append(f"{menit} menit")
            elif counter == 3:
                tmp_tanggal = y.strftime('%d/%m/%y')
                episode.append(tmp_tanggal)
            else:
                episode.append(y)
            counter += 1
        all_episodes.append(episode)

    # Format total durasi untuk ditampilkan di template
    if jam > 0:
        total_durasi_formated = f"{jam} jam {menit} menit"
    else:
        total_durasi_formated = f"{menit} menit"

    context = {
        'is_logged_in': True,
        'role': role,
        'roles': roles,
        'is_premium': check_premium(email),
        'podcaster': nama_podcaster,
        'judul': judul_podcast,
        'tanggal_rilis': tanggal_rilis_formated,
        'tahun_rilis': tahun_rilis,
        'total_durasi': total_durasi_formated,
        'genres': all_genre,
        'episodes': all_episodes
    }

    return render(request, "podcast.html", context)

@csrf_exempt
def create_episode(request, id):
    if "email" not in request.session:
        return redirect('authentication:login')
    
    query_konten = query(f"SELECT * FROM KONTEN WHERE ID='{id}'")
    judul = query_konten[0][1]

    email = request.session["email"]
    role = request.session["role"]
    roles = get_role_pengguna(email)

    if('Podcaster' not in roles):
        return HttpResponseForbidden("Anda Bukan Podcaster!!")

    if request.method == 'POST':
        judul = request.POST.get('title')
        deskripsi = request.POST.get('deskripsi')
        durasi = request.POST.get('durasi')

        id_episode = str(uuid.uuid4())
        today = date.today()

        query(f"""INSERT INTO episode (id_episode, id_konten_podcast, judul, deskripsi, durasi, tanggal_rilis) 
              VALUES ('{id_episode}', '{id}', '{judul}', '{deskripsi}', {durasi}, '{today}')"""
              )

        context = {
            'is_logged_in': True,
            'role': role,
            'roles': roles,
            'is_premium': check_premium(email),
            'judul': judul
        }

        return redirect('podcast:daftar-episode', id=id)

    context = {
        'is_logged_in': True,
        'role': role,
        'roles': roles,
        'is_premium': check_premium(email),
        'judul': judul
    }

    return render(request, "create_episode.html", context)

@csrf_exempt
def create_podcast(request):
    if "email" not in request.session:
        return redirect('authentication:login')
    
    email = request.session["email"]
    role = request.session["role"]
    roles = get_role_pengguna(email)

    if('Podcaster' not in roles):
        return HttpResponseForbidden("Anda Bukan Podcaster!!")

    if request.method == 'POST':
        title = request.POST.get('title')
        genres = request.POST.getlist('genre[]')

        id_konten = str(uuid.uuid4())
        today = date.today()
        current_year = today.year

        query(f"""
            INSERT INTO KONTEN (id, judul, tanggal_rilis, tahun, durasi)
            VALUES ('{id_konten}', '{title}', '{today}', {current_year}, 0)
        """)

        for genre in genres:
            query(f"""
                INSERT INTO GENRE (id_konten, genre)
                VALUES ('{id_konten}', '{genre}')
            """)

        query(f"""
            INSERT INTO PODCAST (id_konten, email_podcaster)
            VALUES ('{id_konten}', '{email}')""")

        context = {
            'is_logged_in': True,
            'role': role,
            'roles': roles,
            'is_premium': check_premium(email)
        }
        return redirect('podcast:list-podcast')
    
    genres = query("SELECT DISTINCT genre FROM GENRE")
    context = {
        'is_logged_in': True,
        'role': role,
        'roles': roles,
        'is_premium': check_premium(email),
        'genres': [genre[0] for genre in genres]
    }
    return render(request, "create_podcast.html", context)

def daftar_podcast(request):
    if "email" not in request.session:
        return redirect('authentication:login')
    
    email = request.session["email"]
    role = request.session["role"]
    roles = get_role_pengguna(email)

    if('Podcaster' not in roles):
        return HttpResponseForbidden("Anda Bukan Podcaster!!")

    get_podcast = query(f"SELECT id_konten FROM PODCAST WHERE EMAIL_PODCASTER='{email}'")
    id_podcast = []
    for i in get_podcast:
        id_podcast.append(str(i[0]))

    data_podcast = []
    for i in id_podcast:
        query_podcast = query(f"SELECT * FROM KONTEN WHERE id = '{i}'")
        podcast = {}
        podcast["id"] = i
        podcast["judul"] = query_podcast[0][1]
        query_total_episode = query(
            f"""
            SELECT id_konten_podcast, COUNT(*)
            FROM episode
            WHERE id_konten_podcast = '{i}'
            GROUP BY id_konten_podcast;
            """
        )
        if(len(query_total_episode)) == 1:
            podcast['total_episode'] = query_total_episode[0][1]
        elif (len(query_total_episode)) == 0:
            podcast['total_episode'] = 0
            
        total_durasi = query_podcast[0][4]
        jam = total_durasi // 60
        menit = total_durasi % 60
        if jam > 0:
            podcast['total_durasi'] = f"{jam} jam {menit} menit"
        else:
            podcast['total_durasi'] = f"{menit} menit"
        data_podcast.append(podcast)

    context = {
        'is_logged_in': True,
        'role': role,
        'roles': roles,
        'is_premium': check_premium(email),
        'data_podcast': data_podcast
    }

    return render(request, "list_podcast.html", context)

def daftar_episode(request, id):
    if "email" not in request.session:
        return redirect('authentication:login')
    
    email = request.session["email"]
    role = request.session["role"]
    roles = get_role_pengguna(email)

    query_konten = query(f"SELECT * FROM KONTEN WHERE ID = '{id}'")
    judul_podcast = query_konten[0][1]
    
    query_episode = query(f"SELECT * FROM EPISODE WHERE ID_KONTEN_PODCAST='{id}'")
    all_episode = []
    for i in query_episode:
        podcast = {}
        podcast["id_episode"] = str(i[0])
        podcast["id_konten"] = str(i[1])
        podcast["judul"] = i[2]
        podcast["deskripsi"] = i[3]
        podcast["durasi"] = i[4]
        podcast["tanggal_rilis"] = i[5]
        all_episode.append(podcast)

    context = {
        'is_logged_in': True,
        'role': role,
        'roles': roles,
        'is_premium': check_premium(email),
        'all_episode': all_episode,
        'judul_podcast': judul_podcast,
        'id': id
    }

    return render(request, "daftar_episode.html", context)

@csrf_exempt
def delete_podcast(request, id):
    if request.method == 'POST':
        query(f"DELETE FROM PODCAST WHERE ID_KONTEN = '{id}'")
        query(f"DELETE FROM KONTEN WHERE ID = '{id}'")
        return JsonResponse({'status': 'success'})
    return HttpResponseNotFound()

@csrf_exempt
def delete_episode(request, id):
    if request.method == 'POST':
        query(f"DELETE FROM EPISODE WHERE ID_EPISODE = '{id}'")
        return JsonResponse({'status': 'success'})
    return HttpResponseNotFound()

def get_podcast_list(request):
    if "email" not in request.session:
        return JsonResponse({'status': 'not_logged_in'}, status=401)
    
    email = request.session["email"]
    get_podcast = query(f"SELECT id_konten FROM PODCAST WHERE EMAIL_PODCASTER='{email}'")
    id_podcast = [str(i[0]) for i in get_podcast]

    data_podcast = []
    for i in id_podcast:
        query_podcast = query(f"SELECT * FROM KONTEN WHERE id = '{i}'")
        podcast = {
            "id": i,
            "judul": query_podcast[0][1],
            "total_episode": query(f"SELECT COUNT(*) FROM episode WHERE id_konten_podcast = '{i}'")[0][0],
            "total_durasi": query_podcast[0][4],
        }
        total_durasi = query_podcast[0][4]
        jam = total_durasi // 60
        menit = total_durasi % 60
        podcast['total_durasi'] = f"{jam} jam {menit} menit" if jam > 0 else f"{menit} menit"
        
        data_podcast.append(podcast)

    return JsonResponse({'data_podcast': data_podcast})


from django.http import JsonResponse

def get_episode_list(request, id):
    query_episode = query(f"SELECT * FROM EPISODE WHERE ID_KONTEN_PODCAST='{id}'")
    all_episode = []
    for i in query_episode:
        episode = {
            "id_episode": str(i[0]),
            "id_konten": str(i[1]),
            "judul": i[2],
            "deskripsi": i[3],
            "durasi": i[4],
            "tanggal_rilis": i[5].strftime('%Y-%m-%d'), 
        }
        all_episode.append(episode)

    return JsonResponse({'all_episode': all_episode})
