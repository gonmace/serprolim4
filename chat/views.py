from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

# Webhook URL
WEBHOOK_URL = 'https://n8npozos.magoreal.com/webhook/chat'

@csrf_exempt
def chat_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_id = data.get('sessionId')
            chat_input = data.get('chatInput')

            if not session_id or not chat_input:
                return JsonResponse({'error': 'Missing sessionId or chatInput'}, status=400)

            # Proxy to n8n
            response = requests.post(WEBHOOK_URL, json={
                'sessionId': session_id,
                'chatInput': chat_input
            }, headers={
                'X-Webhook-Secret': 'ojala-que-las-hojas-no-te-toquen-el-cuerpo-cuando-caigan-2026'
            })

            # Check if n8n response is valid JSON
            try:
                n8n_data = response.json()
                return JsonResponse(n8n_data)
            except json.JSONDecodeError:
                # If n8n returns plain text (or empty), wrap it
                return JsonResponse({'output': response.text})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)
