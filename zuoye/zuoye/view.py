from django.shortcuts import render
from mailbox import Message

from django.template.response import TemplateResponse
# view.py
from django.contrib.auth.views import PasswordResetView
from django.http import JsonResponse
from openai import OpenAI
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .settings import MEDIA_ROOT




from django.shortcuts import render, redirect

from .forms import RegistrationForm, LoginForm

from django.contrib.auth import login as auth_login,authenticate

from django.http import JsonResponse


def wenda(request):
    return render(request, 'wenda.html')
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            # print(user)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    # 设置成功消息
                    # messages.success(request, '注册成功，请登录。')
                    return redirect('home')
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    if request.method == 'POST':
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                User.objects.create_user(username=username, email=email, password=password)
                form1 = LoginForm()
                return render(request, 'login.html',{'form': form1})# Replace 'login_url' with the actual login URL
        else:
            form = RegistrationForm()
        return render(request, 'signup.html', {'form': form})

def home(request):
    csv_file_path = MEDIA_ROOT + '/caipu.csv'
    recipe_list = []
    try:
        csv_data = pd.read_csv(csv_file_path)
        recipe_list = csv_data.to_dict('records')
        # print(recipe_list)
    except Exception as e:
        print(f"Error reading {csv_file_path}: {e}")
    return render(request, 'home.html',{'recipe_list':recipe_list})

@csrf_exempt
def django_view(request):
    context = {'chat_history': ''}

    if request.method == 'POST':
        input_data = request.POST.get("input", "")
        chat_history = request.POST.get("chat_history", "")

        if not input_data:
            return JsonResponse({'error': 'No input data provided'}, status=400)

        messages = [
            {"role": "system", "content": "你是一个精通各种厨艺的资深厨师，你精通每种食物的烹饪技巧，你可以根据他人的提供的身体状态，和食材制定相应的菜谱，你可以在注重味道的同时提供食材的安全的烹饪方式，注意各种食物不会产生食物相克和食物中毒"},
            {"role": "user", "content": input_data},
        ]

        if chat_history:
            # 将历史消息拆分并添加到 messages 列表
            for line in chat_history.split('<div class="ai-message">'):
                if line.strip():
                    messages.append({"role": "user", "content": line.strip()})

        # 从环境变量中获取 API 密钥

        client = OpenAI(api_key="sk-zpsMXNzj2tK4ekxMaYmYEL8fzc8tTcSxB40HYA00f0oVV7PQ", base_url="https://api.moonshot.cn/v1")

        # 定义 CodeRunner 工具
        code_runner_tool = {
            "type": "function",
            "function": {
                "name": "CodeRunner",
                "description": "代码执行器，支持运行 Python 代码",
                "parameters": {
                    "properties": {
                        "language": {"type": "string", "enum": ["python"]},
                        "code": {"type": "string"}
                    },
                    "type": "object"
                }
            }
        }

        # CSV 查询的 Python 代码
        csv_query_code = f"""
        def query_csv(file_path, search_query):
            search_results = []
            try:
                with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                    csv_reader = csv.reader(file)
                    headers = next(csv_reader)
                    for row in csv_reader:
                        if any(search_query.lower() in item.lower() for item in row):
                            search_results.append(row)
                return \"\\n\".join(str(result) for result in search_results) if search_results else \"没有找到匹配的记录。\"
            except Exception as e:
                return str(e)
                """

        # 调用 chat.completions.create 方法
        completion = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=messages,
            function_call={"name": "CodeRunner", "parameters": {
                "language": "python",
                "code": csv_query_code + f'\nquery_csv("caipu.csv", "{input_data}")'
            }},
            temperature=0.3,
        )

        # 获取 CodeRunner 工具的执行结果
        result = completion.choices[0].message.content

        # 格式化结果并添加到 chat_history
        formatted_result = '<div class="ai-message">' + result.replace('\n', '</div><div class="ai-message">') + '</div>'
        context['chat_history'] += '<div class="message user-message">' + input_data + '</div>' + formatted_result

    return render(request, 'wenda.html', context)


from django.contrib import messages
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 可以选择在这里登录用户
            auth_login(request, user)
            # 设置成功消息
            messages.success(request, '注册成功，请登录。')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # 这里使用 login 函数登录用户
            user = form.get_user()
            auth_login(request, user)
            # 设置成功消息
            messages.success(request, '登录成功。')
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})




def terms_view(request):
    # 渲染服务条款页面
    return render(request, 'terms.html')



import pandas as pd
from django.shortcuts import render


def home_view1(request):
    csv_file_path = MEDIA_ROOT+'/caipu.csv'
    recipe_list = []
    try:
        csv_data = pd.read_csv(csv_file_path)
        recipe_list = csv_data.to_dict('records')
        # print(recipe_list)
    except Exception as e:
        print(f"Error reading {csv_file_path}: {e}")
    return JsonResponse({'recipe_list': recipe_list})

def home_view(request):
    # 假设用户通过查询参数提交搜索关键词
    search_query = request.GET.get('search_query', '')
    csv_file_path = MEDIA_ROOT + '/caipu.csv'
    recipe_list = []
    try:
        csv_data = pd.read_csv(csv_file_path)
        if search_query:
            # 根据搜索关键词过滤数据
            filtered_data = csv_data[csv_data['name'].str.contains(search_query, case=False, na=False)]
            recipe_list = filtered_data.to_dict('records')
        else:
            # 如果没有搜索关键词，返回所有数据
            recipe_list = csv_data.to_dict('records')
    except Exception as e:
        print(f"Error reading {csv_file_path}: {e}")
    return JsonResponse({'recipe_list': recipe_list})