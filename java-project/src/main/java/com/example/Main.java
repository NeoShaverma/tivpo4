package com.example;

import java.util.List;
import java.util.Scanner;

/**
 * Главный класс приложения - Система управления библиотекой
 */
public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Library library = new Library();
        FileManager fileManager = new FileManager();
        
        // Загрузка данных из файла
        try {
            List<Book> loadedBooks = fileManager.loadLibraryData();
            for (Book book : loadedBooks) {
                library.addBook(book);
            }
            System.out.println("Данные загружены из файла.");
        } catch (Exception e) {
            System.out.println("Ошибка при загрузке данных: " + e.getMessage());
        }
        
        // Добавление тестовых книг
        library.addBook(new Book("978-5-17-123456", "Война и мир", "Лев Толстой", 1869));
        library.addBook(new Book("978-5-17-123457", "Преступление и наказание", "Фёдор Достоевский", 1866));
        library.addBook(new Book("978-5-17-123458", "Мастер и Маргарита", "Михаил Булгаков", 1967));
        
        System.out.println("\n=== Система управления библиотекой ===");
        System.out.println("1. Показать все книги");
        System.out.println("2. Выдать книгу");
        System.out.println("3. Вернуть книгу");
        System.out.println("4. Найти книги по автору");
        System.out.println("5. Показать логи");
        System.out.println("6. Сохранить данные");
        System.out.println("0. Выход");
        
        boolean running = true;
        while (running) {
            System.out.print("\nВыберите действие: ");
            try {
                int choice = scanner.nextInt();
                scanner.nextLine();
            
            switch (choice) {
                case 1:
                    System.out.println("Всего книг: " + library.getBookCount());
                    break;
                    
                case 2:
                    System.out.print("Введите ISBN книги: ");
                    String isbn = scanner.nextLine();
                    System.out.print("Введите имя читателя: ");
                    String reader = scanner.nextLine();
                    if (library.borrowBook(isbn, reader)) {
                        System.out.println("Книга успешно выдана!");
                    } else {
                        System.out.println("Не удалось выдать книгу.");
                    }
                    break;
                    
                case 3:
                    System.out.print("Введите ISBN книги: ");
                    String returnIsbn = scanner.nextLine();
                    if (library.returnBook(returnIsbn)) {
                        System.out.println("Книга успешно возвращена!");
                    } else {
                        System.out.println("Не удалось вернуть книгу.");
                    }
                    break;
                    
                case 4:
                    System.out.print("Введите имя автора (или Enter для всех): ");
                    String author = scanner.nextLine();
                    // RUNTIME ОШИБКА: Если пользователь нажмёт Enter, author будет пустой строкой
                    // Но если передать null явно, будет NPE в findBooksByAuthor
                    if (author.isEmpty()) {
                        author = null;  // RUNTIME ОШИБКА: передача null вызовет NPE
                    }
                    List<Book> foundBooks = library.findBooksByAuthor(author);
                    System.out.println("Найдено книг: " + foundBooks.size());
                    for (Book book : foundBooks) {
                        System.out.println("  - " + book);
                    }
                    break;
                    
                case 5:
                    List<String> logs = library.getLogEntries();
                    System.out.println("Последние 10 записей:");
                    int start = Math.max(0, logs.size() - 10);
                    for (int i = start; i < logs.size(); i++) {
                        System.out.println("  " + logs.get(i));
                    }
                    break;
                    
                case 6:
                    try {
                        List<Book> allBooks = library.getAllBooks();
                        fileManager.saveLibraryData(allBooks);
                        System.out.println("Данные сохранены.");
                    } catch (Exception e) {
                        System.out.println("Ошибка при сохранении: " + e.getMessage());
                    }
                    break;
                    
                case 0:
                    running = false;
                    System.out.println("До свидания!");
                    break;
                    
                default:
                    System.out.println("Неверный выбор!");
            }
            } catch (java.util.InputMismatchException e) {
                System.out.println("Ошибка: введите число!");
                scanner.nextLine(); // Очистка буфера
            }
        }
        
        scanner.close();
    }
}

