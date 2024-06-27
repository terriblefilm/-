from django.http import JsonResponse
from openai import OpenAI
from django.views.decorators.csrf import csrf_exempt
import os

@csrf_exempt
def your_django_view(request):
    client = OpenAI(api_key="sk-zpsMXNzj2tK4ekxMaYmYEL8fzc8tTcSxB40HYA00f0oVV7PQ", base_url="https://api.moonshot.cn/v1")
    if request.method == 'POST':
        input_data = request.POST.get('input_data')
        if input_data:
            completion = client.chat.completions.create(
                model="moonshot-v1-8k",
            messages=[
                {
                 "role": "system",
                 "content": "你是一个精通各种厨艺的资深厨师，你精通每种食物的烹饪技巧，你可以根据他人的提供的身体状态，和食材制定相应的菜谱，你可以在注重味道的同时提供食材的安全的烹饪方式，注意各种食物不会产生食物相克和食物中毒"},
                {"role": "user", "content": input_data}
            ],
            temperature=0.3,
        )
            result = completion.choices[0].message.content
            return JsonResponse({'message': result})
        else:
            return JsonResponse({'error': 'No input data provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


