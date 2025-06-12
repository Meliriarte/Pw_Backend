from flask import Flask, request, jsonify
from flask_cors import CORS
from models import Task, initialize_db, close_db
import os

# Inicializar Flask
app = Flask(__name__)
CORS(app, origins=["*"])  # Permitir todas las origins para GitHub Pages

# Inicializar base de datos
initialize_db()

@app.route("/")
def health_check():
    return {"status": "ok", "message": "Todo API running successfully"}

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Obtener todas las tareas"""
    try:
        tasks = Task.select()
        return jsonify([task_to_dict(task) for task in tasks])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tasks', methods=['POST'])
def create_task():
    """Crear una nueva tarea"""
    try:
        data = request.get_json()
        
        if not data or 'title' not in data:
            return jsonify({"error": "Title is required"}), 400
            
        task = Task.create(
            title=data['title'],
            done=data.get('done', False)
        )
        return jsonify(task_to_dict(task)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Actualizar una tarea existente"""
    try:
        task = Task.get_by_id(task_id)
        data = request.get_json()
        
        if 'title' in data:
            task.title = data['title']
        if 'done' in data:
            task.done = data['done']
            
        task.save()
        return jsonify(task_to_dict(task))
    except Task.DoesNotExist:
        return jsonify({"error": "Task not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Eliminar una tarea"""
    try:
        task = Task.get_by_id(task_id)
        task.delete_instance()
        return jsonify({"message": "Task deleted successfully"})
    except Task.DoesNotExist:
        return jsonify({"error": "Task not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def task_to_dict(task):
    """Convertir modelo Task a diccionario"""
    return {
        "id": task.id,
        "title": task.title,
        "done": task.done
    }

@app.teardown_appcontext
def close_db_connection(error):
    close_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
