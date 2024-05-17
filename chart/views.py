from django.shortcuts import redirect, render

from authentication.views import check_premium, get_role_pengguna
from utils.query import query

def daftar_chart(request):
    if "email" not in request.session:
        return redirect('authentication:login')
    
    email = request.session["email"]
    role = request.session["role"]
    roles = get_role_pengguna(email)

    query_charts = query(f"SELECT * FROM chart")
    all_chart = []
    for i in query_charts:
        chart = []
        for y in i:
            chart.append(str(y))
        all_chart.append(chart)

    context = {
        'is_logged_in': True,
        'role': role,
        'roles': roles,
        'is_premium': check_premium(email),
        'charts': all_chart
    }
    return render(request, "chart_list.html", context)

def detail_chart(request, id, tipe):
    if "email" not in request.session:
        return redirect('authentication:login')
    
    email = request.session["email"]
    role = request.session["role"]
    roles = get_role_pengguna(email)

    query(f"DELETE FROM PLAYLIST_SONG WHERE id_playlist='{id}'")
    query(f"""INSERT INTO PLAYLIST_SONG (id_playlist, id_song)
            SELECT DISTINCT '{id}'::uuid, subquery.id_konten
            FROM (
                SELECT id_konten, total_play
                FROM SONG
                ORDER BY total_play DESC
                LIMIT 20
            ) AS subquery;
        """)
    
    searched_table = query(f"""SELECT distinct K.judul, A.nama, K.tanggal_rilis, S.total_play, K.id
                            FROM AKUN A, PLAYLIST_SONG P, ARTIST R, SONG S, KONTEN K
                            WHERE P.id_playlist = '{id}' AND 
                                R.email_akun = A.email AND 
                                S.id_konten=P.id_song AND 
                                K.id = P.id_song AND 
                                S.id_artist = R.id AND
                                K.id = S.id_konten
                            ORDER BY S.total_play DESC
                            """)
    all_table = []
    for i in searched_table:
        song = {}
        song["judul"] = i[0]
        song["email"] = i[1]
        song["tanggal_rilis"] = i[2]
        song["total_play"] = i[3]
        song["id"] = str(i[4])
        all_table.append(song)

    context = {
        'is_logged_in': True,
        'role': role,
        'roles': roles,
        'tipe': tipe,
        'is_premium': check_premium(email),
        'data_table': all_table
    }

    return render(request, "chart_detail.html", context)
