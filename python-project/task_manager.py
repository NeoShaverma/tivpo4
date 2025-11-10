"""
Модуль для управления задачами
"""

from datetime import datetime, timedelta
from task import Task, Priority, TaskStatus
from collections import defaultdict

class TaskManager:
    """Класс для управления задачами"""
    
    def __init__(self):
        self.tasks = []
        self.next_id = 1
        self.history = []
        self.statistics = defaultdict(int)
    
    def add_task(self, title, description="", priority=Priority.MEDIUM, deadline=None):
        """Добавляет новую задачу"""
        task = Task(title, description, priority, deadline)
        task.id = self.next_id
        self.next_id += 1
        self.tasks.append(task)
        self.history.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Создана задача: {title}")
        self.statistics['total_created'] += 1
        return task.id
    
    def get_task(self, task_id):
        """Получает задачу по ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task_status(self, task_id, status):
        """Обновляет статус задачи"""
        task = self.get_task(task_id)
        if not task:
            self.history.append(f"Попытка обновить несуществующую задачу: {task_id}")
            return False
        
        old_status = task.status
        if status == TaskStatus.DONE:
            task.mark_done()
            self.statistics['total_completed'] += 1
        elif status == TaskStatus.IN_PROGRESS:
            task.mark_in_progress()
        elif status == TaskStatus.CANCELLED:
            task.cancel()
            self.statistics['total_cancelled'] += 1
        
        self.history.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Задача '{task.title}': {old_status.value} -> {status.value}")
        return True
    
    def delete_task(self, task_id):
        """Удаляет задачу"""
        task = self.get_task(task_id)
        if not task:
            return False
        
        self.tasks.remove(task)
        self.history.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Удалена задача: {task.title}")
        self.statistics['total_deleted'] += 1
        return True
    
    def get_tasks_by_status(self, status):
        """Получает задачи по статусу"""
        return [task for task in self.tasks if task.status == status]
    
    def get_tasks_by_priority(self, priority):
        """Получает задачи по приоритету"""
        return [task for task in self.tasks if task.priority == priority]
    
    def get_overdue_tasks(self):
        """Получает просроченные задачи"""
        return [task for task in self.tasks if task.is_overdue()]
    
    def get_statistics(self):
        """Получает статистику по задачам"""
        total_tasks = len(self.tasks)
        # RUNTIME ОШИБКА #2: Деление на ноль при пустом списке задач
        # Проверка есть выше, но деление выполняется без проверки
        stats = {
            'total': len(self.tasks),
            'todo': len(self.get_tasks_by_status(TaskStatus.TODO)),
            'in_progress': len(self.get_tasks_by_status(TaskStatus.IN_PROGRESS)),
            'done': len(self.get_tasks_by_status(TaskStatus.DONE)),
            'overdue': len(self.get_overdue_tasks()),
            'avg_completion': self.statistics['total_completed'] / total_tasks,  # RUNTIME ОШИБКА: деление на ноль если total_tasks == 0
            **self.statistics
        }
        return stats
    
    def get_history(self, limit=10):
        """Получает последние записи истории"""
        # RUNTIME ОШИБКА #1: Утечка памяти - история накапливается без ограничений
        # Нет механизма очистки старых записей
        return self.history[-limit:] if limit > 0 else self.history

