from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import MySQLdb


def get_connection():
    return MySQLdb.connect(
        host=settings.DATABASES['default']['HOST'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        database=settings.DATABASES['default']['NAME'],
        charset='utf8'
    )


def task_list_page(request):
    return render(request, 'task_list.html')


def add_task_page(request):
    return render(request, 'add_task.html')


def api_get_tasks(request):
    try:
        # ==============================
        # 🔹 DataTables Params
        # ==============================
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))      # OFFSET
        length = int(request.GET.get("length", 10))  # LIMIT
        search_value = request.GET.get("search[value]", "").strip()

        conn = get_connection()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)

        # ==============================
        # 🔹 Search filter
        # ==============================
        where = ""
        params = []

        if search_value:
            where = """
                WHERE 
                    title LIKE %s 
                    OR description LIKE %s 
                    OR due_date LIKE %s 
                    OR status LIKE %s
            """
            params = [
                f"%{search_value}%",
                f"%{search_value}%",
                f"%{search_value}%",
                f"%{search_value}%"
            ]

        # ==============================
        # 🔹 Total Records (without filter)
        # ==============================
        cursor.execute("SELECT COUNT(*) as cnt FROM tasks")
        total_records = cursor.fetchone()["cnt"]

        # ==============================
        # 🔹 Total Records (with filter)
        # ==============================
        cursor.execute(
            f"SELECT COUNT(*) as cnt FROM tasks {where}",
            params
        )
        filtered_records = cursor.fetchone()["cnt"]

        # ==============================
        # 🔹 Fetch paginated data
        # ==============================
        cursor.execute(
            f"""
            SELECT id, title, description, due_date, status
            FROM tasks
            {where}
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
            """,
            params + [length, start]
        )

        tasks = cursor.fetchall()

        cursor.close()
        conn.close()

        # ==============================
        # 🔹 DataTables Response
        # ==============================
        return JsonResponse({
            "draw": draw,
            "recordsTotal": total_records,
            "recordsFiltered": filtered_records,
            "data": tasks
        })

    except Exception as e:
        print("Error:", e)
        return JsonResponse({
            "draw": draw,
            "recordsTotal": 0,
            "recordsFiltered": 0,
            "data": [],
            "error": str(e)
        }, status=500)


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


def api_get_task_by_id(request, task_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute(
            "SELECT id, title, description, due_date, status FROM tasks WHERE id = %s",
            (task_id,)
        )

        task = cursor.fetchone()

        if not task:
            return JsonResponse({'error': 'Task not found'}, status=404)

        return JsonResponse({'task': task}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


def api_update_task(request, task_id):

    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    try:
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        status = request.POST.get('status')

        # Validation
        if not title or not description or not due_date or not status:
            return JsonResponse(
                {'error': 'All fields are required'},
                status=400
            )

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE tasks
            SET title=%s,
                description=%s,
                due_date=%s,
                status=%s
            WHERE id=%s
        """, (title, description, due_date, status, task_id))

        conn.commit()

        return JsonResponse(
            {'message': 'Task updated successfully'},
            status=200
        )

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


def api_delete_task(request, task_id):
    try:
        if request.method != 'POST':
            return JsonResponse({'error': 'Invalid request'}, status=400)
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return JsonResponse({'message': 'Task Deleted Successfully...'})
    
    except Exception as e:
        return JsonResponse(
            {'error': str(e)},
            status=500
        )


