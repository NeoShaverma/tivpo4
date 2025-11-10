"""
Главный модуль приложения - Система управления задачами
"""

from datetime import datetime, timedelta
from task_manager import TaskManager
from storage import TaskStorage
from task import Priority, TaskStatus

def print_menu():
    """Выводит меню приложения"""
    print("\n=== Система управления задачами ===")
    print("1. Добавить задачу")
    print("2. Показать все задачи")
    print("3. Показать задачи по статусу")
    print("4. Показать задачи по приоритету")
    print("5. Показать просроченные задачи")
    print("6. Обновить статус задачи")
    print("7. Удалить задачу")
    print("8. Показать статистику")
    print("9. Показать историю")
    print("10. Сохранить задачи")
    print("11. Экспортировать в текст")
    print("0. Выход")

def main():
    manager = TaskManager()
    storage = TaskStorage()
    
    # Загрузка задач из файла
    loaded_tasks = storage.load_tasks()
    for task in loaded_tasks:
        manager.tasks.append(task)
        if task.id and task.id >= manager.next_id:
            manager.next_id = task.id + 1
    if loaded_tasks:
        print(f"Загружено задач: {len(loaded_tasks)}")
    
    # Добавление тестовых задач
    manager.add_task("Изучить Python", "Изучить основы языка Python", Priority.HIGH, 
                     datetime.now() + timedelta(days=7))
    manager.add_task("Сделать практическую работу", "Выполнить практическую работу №4", 
                     Priority.URGENT, datetime.now() + timedelta(days=3))
    manager.add_task("Купить продукты", "", Priority.MEDIUM)
    
    running = True
    while running:
        print_menu()
        try:
            choice = input("\nВыберите действие: ").strip()
            
            if choice == "1":
                title = input("Название задачи: ")
                description = input("Описание (необязательно): ")
                print("Приоритет: 1-Низкий, 2-Средний, 3-Высокий, 4-Срочный")
                priority_num = int(input("Выберите приоритет (1-4): "))
                priority = Priority(priority_num)
                
                deadline_input = input("Дедлайн (дд.мм.гггг или Enter для пропуска): ")
                deadline = None
                if deadline_input:
                    deadline = datetime.strptime(deadline_input, "%d.%m.%Y")
                
                task_id = manager.add_task(title, description, priority, deadline)
                print(f"Задача добавлена с ID: {task_id}")
            
            elif choice == "2":
                tasks = manager.tasks
                if not tasks:
                    print("Нет задач")
                else:
                    for task in tasks:
                        print(f"ID: {task.id} - {task}")
            
            elif choice == "3":
                print("Статусы: 1-TODO, 2-IN_PROGRESS, 3-DONE, 4-CANCELLED")
                status_num = int(input("Выберите статус: "))
                if 1 <= status_num <= len(TaskStatus):
                    status = list(TaskStatus)[status_num - 1]
                    tasks = manager.get_tasks_by_status(status)
                    print(f"\nЗадач со статусом {status.value}: {len(tasks)}")
                    for task in tasks:
                        print(f"  ID: {task.id} - {task}")
                else:
                    print("Неверный номер статуса")
            
            elif choice == "4":
                print("Приоритеты: 1-Низкий, 2-Средний, 3-Высокий, 4-Срочный")
                priority_num = int(input("Выберите приоритет: "))
                priority = Priority(priority_num)
                tasks = manager.get_tasks_by_priority(priority)
                print(f"\nЗадач с приоритетом {priority.name}: {len(tasks)}")
                for task in tasks:
                    print(f"  ID: {task.id} - {task}")
            
            elif choice == "5":
                overdue = manager.get_overdue_tasks()
                if not overdue:
                    print("Нет просроченных задач")
                else:
                    print(f"\nПросроченных задач: {len(overdue)}")
                    for task in overdue:
                        print(f"  ID: {task.id} - {task}")
            
            elif choice == "6":
                task_id = int(input("ID задачи: "))
                print("Статусы: 1-TODO, 2-IN_PROGRESS, 3-DONE, 4-CANCELLED")
                status_num = int(input("Новый статус: "))
                status = list(TaskStatus)[status_num - 1]
                if manager.update_task_status(task_id, status):
                    print("Статус обновлён")
                else:
                    print("Задача не найдена")
            
            elif choice == "7":
                task_id = int(input("ID задачи для удаления: "))
                if manager.delete_task(task_id):
                    print("Задача удалена")
                else:
                    print("Задача не найдена")
            
            elif choice == "8":
                stats = manager.get_statistics()
                print("\n=== Статистика ===")
                print(f"Всего задач: {stats['total']}")
                print(f"  TODO: {stats['todo']}")
                print(f"  В работе: {stats['in_progress']}")
                print(f"  Выполнено: {stats['done']}")
                print(f"  Просрочено: {stats['overdue']}")
                print(f"\nСоздано: {stats['total_created']}")
                print(f"Завершено: {stats['total_completed']}")
                print(f"Отменено: {stats['total_cancelled']}")
            
            elif choice == "9":
                history = manager.get_history(15)
                print("\n=== История ===")
                for entry in history:
                    print(f"  {entry}")
            
            elif choice == "10":
                storage.save_tasks(manager.tasks)
                print("Задачи сохранены")
            
            elif choice == "11":
                filename = input("Имя файла для экспорта (по умолчанию tasks_export.txt): ").strip()
                if not filename:
                    filename = "tasks_export.txt"
                storage.export_to_text(manager.tasks, filename)
                print(f"Задачи экспортированы в {filename}")
            
            elif choice == "0":
                # Автосохранение при выходе
                storage.save_tasks(manager.tasks)
                print("До свидания!")
                running = False
            
            else:
                print("Неверный выбор!")
        
        except ValueError as e:
            print(f"Ошибка ввода: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
