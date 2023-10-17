from dataclasses import dataclass
from email import message
from traceback import print_tb
from django.shortcuts import render
from .models import sql_models,put_log
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings


# Create your views here.
def devTemplate(request):
    return render(request, 'index.html')

def test_error(request):
    return render(request, 'test_error.html')

def test_login(request):
    if request.method == "POST":
        user_records = sql_models.login_check(request.POST)
        if not user_records:
            message = "社員番号もしくはパスワードに誤りがあります。"
            return render(request, 'index.html', context={
                "message" : message
            })
        else:
            return search_first(request,user_records)
    else:
        return render(request, 'test_error.html')


def search_first(request,user_records):
    user_records = {
        "mits_username": user_records[0][0],
        "mits_password": user_records[0][1],
        "staff_no": user_records[0][2],
        "staff_name":user_records[0][3],
        "staff_section":user_records[0][4]
    }
    data_obj = {
        'user_records' : user_records
    }
    #セッションに保存
    request.session['data_obj'] = data_obj
    main_url = settings.MAIN_PAGE_URL # メインページに遷移させる
    response = redirect(main_url) 

    #ここからログ吐き出し開始
    log_path = settings.LOGS_PATH

    if log_path:
        put_log(log_path,data_obj)  

    return response

def search(request):
    return render(request, 'search.html')

def logout(request):
    request.session.clear()
    return redirect('.')
