from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Создание объекта GoogleAuth и авторизация через веб-сервер
gauth = GoogleAuth()
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

# csrf_exempt используется, чтобы отключить проверку CSRF.
#@csrf_exempt
def create_google_drive_document(request):
    if request.method == 'POST':
        try:
            # Получение данных из тела POST-запроса
            data = json.loads(request.body.decode('utf-8'))
            file_data = data.get('data')
            file_name = data.get('name')

            # Создание объекта GoogleDrive с использованием авторизации GoogleAuth
            drive = GoogleDrive(gauth)

            # Создание объекта файла и установка его содержимого
            file = drive.CreateFile({'title': file_name})
            file.SetContentString(file_data)

            # Загрузка файла на Google Drive
            file.Upload()

            return JsonResponse({'message': 'Файл успешно загружен на Google диск'})

        except Exception as e:
            # Возвращение ошибки в случае исключения
            return JsonResponse({'error': str(e)}, status=500)

    # Возвращение ошибки в случае использования неразрешенного метода
    return JsonResponse({'error': 'Invalid method'}, status=400)
