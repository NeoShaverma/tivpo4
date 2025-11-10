package com.example;

import java.util.*;

/**
 * Класс для управления библиотекой книг
 */
public class Library {
    private Map<String, Book> books;
    private Map<String, List<String>> borrowHistory;
    private List<String> logEntries;
    
    public Library() {
        books = new HashMap<>();
        borrowHistory = new HashMap<>();
        logEntries = new ArrayList<>();
        // RUNTIME ОШИБКА #1: Утечка памяти - logEntries растёт без ограничений
        // Нет механизма ограничения размера истории
    }
    
    /**
     * Добавляет книгу в библиотеку
     */
    public void addBook(Book book) {
        if (book == null) {
            logEntries.add("Попытка добавить null книгу");
            return;
        }
        if (books.containsKey(book.getIsbn())) {
            logEntries.add("Попытка добавить дубликат книги: " + book.getIsbn());
            return;
        }
        books.put(book.getIsbn(), book);
        logEntries.add("Добавлена книга: " + book.getTitle());
    }
    
    /**
     * Выдаёт книгу читателю
     */
    public boolean borrowBook(String isbn, String readerName) {
        Book book = books.get(isbn);
        if (book == null) {
            logEntries.add("Книга не найдена: " + isbn);
            return false;
        }
        
        if (!book.isAvailable()) {
            logEntries.add("Книга уже выдана: " + book.getTitle());
            return false;
        }
        
        book.setAvailable(false);
        if (!borrowHistory.containsKey(readerName)) {
            borrowHistory.put(readerName, new ArrayList<>());
        }
        borrowHistory.get(readerName).add(isbn);
        logEntries.add("Книга выдана: " + book.getTitle() + " читателю: " + readerName);
        return true;
    }
    
    /**
     * Возвращает книгу в библиотеку
     */
    public boolean returnBook(String isbn) {
        Book book = books.get(isbn);
        if (book == null) {
            logEntries.add("Книга не найдена: " + isbn);
            return false;
        }
        
        if (book.isAvailable()) {
            logEntries.add("Книга уже в библиотеке: " + book.getTitle());
            return false;
        }
        
        book.setAvailable(true);
        logEntries.add("Книга возвращена: " + book.getTitle());
        return true;
    }
    
    /**
     * Поиск книг по автору
     */
    public List<Book> findBooksByAuthor(String author) {
        List<Book> result = new ArrayList<>();
        // RUNTIME ОШИБКА #2: NullPointerException - если author == null, equalsIgnoreCase упадёт
        // Нет проверки author на null перед использованием
        for (Book book : books.values()) {
            // RUNTIME ОШИБКА: Если author == null, то equalsIgnoreCase вызовет NPE
            // (хотя equalsIgnoreCase принимает null, но лучше проверить для безопасности)
            if (book.getAuthor() != null && book.getAuthor().equalsIgnoreCase(author)) {
                result.add(book);
            }
        }
        // RUNTIME ОШИБКА #3: Проблема производительности - линейный поиск O(n) при каждом запросе
        // Нет индексации по автору, поиск выполняется по всем книгам
        return result;
    }
    
    /**
     * Получить историю выдачи для читателя
     */
    public List<String> getBorrowHistory(String readerName) {
        return borrowHistory.getOrDefault(readerName, new ArrayList<>());
    }
    
    /**
     * Получить все логи
     */
    public List<String> getLogEntries() {
        return logEntries;
    }
    
    /**
     * Получить количество книг
     */
    public int getBookCount() {
        return books.size();
    }
    
    /**
     * Получить все книги
     */
    public List<Book> getAllBooks() {
        return new ArrayList<>(books.values());
    }
}

