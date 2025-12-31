from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import MySQLdb
import json

# Helper function for DB connection
def get_connection():
    return MySQLdb.connect(
        host=settings.DATABASES['default']['HOST'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        database=settings.DATABASES['default']['NAME'],
        charset='utf8'
    )

# ------------------ Template Views ------------------

def task_list_page(request):
    return render(request, 'task_list.html')

def add_task_page(request):
    return render(request, 'add_task.html')

# ------------------ API Views ------------------

def search_created_task(request):
    conn = get_connection()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return JsonResponse({'tasks': tasks})

def api_create_task(request):

    if request.method != 'POST':    
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    try:
    
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        status = request.POST.get('status')

        # ---- Validation ----
        if not title or not description or not due_date or not status:
            return JsonResponse(
                {'error': 'All fields are required'},
                status=400
            )
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO tasks (title, description, due_date, status, created_at)
            VALUES (%s, %s, %s, %s, NOW())
            """,
            (title, description, due_date, status)
        )

        conn.commit()

        return JsonResponse(
            {'message': 'Task created successfully'},
            status=200
        )
    except Exception as e:
        return JsonResponse(
            {'error': str(e)},
            status=500
        )

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

def api_update_task(request, task_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET status=%s WHERE id=%s",
            (data['status'], task_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return JsonResponse({'message': 'Task updated successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def api_delete_task(request, task_id):
    if request.method == 'POST':
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return JsonResponse({'message': 'Task deleted successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
