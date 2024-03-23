from django.shortcuts import render
from django.shortcuts import render, HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def user_list(request):
    name = "卷云"
    roles = ["卷云", "高积云", "钩卷云"]
    user_info = {"name": "lucy", "age": 20, "role": "teacher"}

    return render(
        request,
        'user_list.html',
        {
            "n1": name,
            "r1": roles,
            "u1": user_info
        }
    )


def yun_guan(request):
    return render(request, 'yun_guan.html')
