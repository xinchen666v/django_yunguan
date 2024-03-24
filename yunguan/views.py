from django.shortcuts import render, HttpResponse
from .api import yun_guan_api
from django.core.files.storage import default_storage
import base64
from django.core.files.base import ContentFile


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
