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

    query_charts = query(f"SELECT * FROM chart WHERE id_playlist = '{id}'")
    tipe_chart = query_charts
    print(tipe_chart)

    context = {
        'is_logged_in': True,
        'role': role,
        'roles': roles,
        'tipe': tipe,
        'is_premium': check_premium(email)
    }

    return render(request, "chart_detail.html", context)
