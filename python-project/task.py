"""
Модуль для представления задачи
"""

from datetime import datetime
from enum import Enum

class Priority(Enum):
    """Приоритет задачи"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

class TaskStatus(Enum):
    """Статус задачи"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"

class Task:
    """Класс, представляющий задачу"""
    
    def __init__(self, title, description="", priority=Priority.MEDIUM, deadline=None):
        self.id = None
        self.title = title
        self.description = description
        self.priority = priority
        self.status = TaskStatus.TODO
        self.deadline = deadline
        self.created_at = datetime.now()
        self.completed_at = None
    
    def mark_done(self):
        """Отмечает задачу как выполненную"""
        self.status = TaskStatus.DONE
        self.completed_at = datetime.now()
    
    def mark_in_progress(self):
        """Отмечает задачу как выполняемую"""
        self.status = TaskStatus.IN_PROGRESS
    
    def cancel(self):
        """Отменяет задачу"""
        self.status = TaskStatus.CANCELLED
    
    def is_overdue(self):
        """Проверяет, просрочена ли задача"""
        if self.deadline and self.status != TaskStatus.DONE:
            return datetime.now() > self.deadline
        return False
    
    def __str__(self):
        status_icon = {
            TaskStatus.TODO: "📋",
            TaskStatus.IN_PROGRESS: "🔄",
            TaskStatus.DONE: "✅",
            TaskStatus.CANCELLED: "❌"
        }
        priority_icon = {
            Priority.LOW: "🟢",
            Priority.MEDIUM: "🟡",
            Priority.HIGH: "🟠",
            Priority.URGENT: "🔴"
        }
        
        icon = status_icon.get(self.status, "📋")
        priority = priority_icon.get(self.priority, "🟡")
        deadline_str = f" (до {self.deadline.strftime('%d.%m.%Y')})" if self.deadline else ""
        overdue = " ⚠️ ПРОСРОЧЕНО" if self.is_overdue() else ""
        
        return f"{icon} {priority} {self.title}{deadline_str}{overdue}"

