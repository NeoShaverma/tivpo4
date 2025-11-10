"""
Модуль для сохранения и загрузки задач
"""

import json
from datetime import datetime
from task import Task, Priority, TaskStatus

class TaskStorage:
    """Класс для работы с файловым хранилищем задач"""
    
    def __init__(self, filename="tasks.json"):
        self.filename = filename
    
    def save_tasks(self, tasks):
        """Сохраняет задачи в JSON файл"""
        tasks_data = []
        for task in tasks:
            task_dict = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'priority': task.priority.value,
                'status': task.status.value,
                'created_at': task.created_at.isoformat(),
                'deadline': task.deadline.isoformat() if task.deadline else None,
                'completed_at': task.completed_at.isoformat() if task.completed_at else None
            }
            tasks_data.append(task_dict)
        
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(tasks_data, file, ensure_ascii=False, indent=2)
    
    def load_tasks(self):
        """Загружает задачи из JSON файла"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                tasks_data = json.load(file)
            
            tasks = []
            for task_dict in tasks_data:
                # RUNTIME ОШИБКА #3: Некорректная обработка исключений - при повреждённом JSON может упасть
                task = Task(
                    task_dict.get('title', ''),
                    task_dict.get('description', ''),
                    Priority(task_dict.get('priority', 2)),
                    datetime.fromisoformat(task_dict['deadline']) if task_dict.get('deadline') else None
                )
                task.id = task_dict.get('id')
                # Если status неверный, TaskStatus() вызовет ValueError, но он не обрабатывается
                task.status = TaskStatus(task_dict.get('status', 'todo'))
                task.created_at = datetime.fromisoformat(task_dict.get('created_at', datetime.now().isoformat()))
                if task_dict.get('completed_at'):
                    task.completed_at = datetime.fromisoformat(task_dict['completed_at'])
                tasks.append(task)
            
            return tasks
        except FileNotFoundError:
            return []
        except (KeyError, ValueError, TypeError) as e:
            # RUNTIME ОШИБКА: Обработка слишком общая, может скрыть конкретные проблемы
            print(f"Ошибка при загрузке задач: {e}")
            return []
    
    def export_to_text(self, tasks, filename="tasks_export.txt"):
        """Экспортирует задачи в текстовый файл"""
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("=== СПИСОК ЗАДАЧ ===\n\n")
            for task in tasks:
                file.write(f"{task}\n")
                if task.description:
                    file.write(f"   Описание: {task.description}\n")
                file.write("\n")

