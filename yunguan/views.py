from django.shortcuts import render, HttpResponse, redirect
from .api import yun_guan_api
from django.core.files.storage import default_storage
import base64
from django.core.files.base import ContentFile
from django.contrib import messages
from .models import User
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password


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


# def yun_guan(request):
#     if request.method == 'POST':
#         image_file = request.FILES['image']
#         result = yun_guan_api(image_file)  # 使用上传的图片文件调用API
#         return HttpResponse(result)  # 返回识别结果
#     return render(request, 'upload.html')  # 显示上传表单的页面


def yun_guan(request):
    if request.method == 'POST' and request.FILES['image']:
        image_file = request.FILES['image']
        # 保存文件到服务器
        file_name = default_storage.save(image_file.name, ContentFile(image_file.read()))
        file_path = default_storage.path(file_name)

        # 读取文件并进行BASE64编码
        with open(file_path, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            base64_str = base64_data.decode('UTF8')

        # 删除临时保存的文件
        default_storage.delete(file_name)

        # 调用API并获取结果
        result = yun_guan_api(base64_str)
        return render(request, 'result.html', {'results': result})

    return render(request, 'upload.html')


def login(request):
    return render(request, 'login.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username).first()
        if user and check_password(password, user.password):
            # 用户验证成功，可以在这里设置session或者其他登录后的逻辑
            return redirect('/yun_guan/')  # 假设有一个名为'home'的路由
        else:
            # 用户验证失败，返回错误信息
            return render(request, 'login.html', {'error': '用户名或密码错误'})
    else:
        # 非POST请求，显示登录页面
        return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            return render(request, 'login.html', {'error': '用户名已存在'})
        elif User.objects.filter(email=email).exists():
            return render(request, 'login.html', {'error': '邮箱已存在'})
        else:
            encrypted_password = make_password(password)
            User.objects.create(username=username, email=email, password=encrypted_password)
            return redirect('/login/')  # 注册成功后重定向到登录页面
    else:
        return render(request, 'login.html')