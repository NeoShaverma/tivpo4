package com.example;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

/**
 * Класс для работы с файлами библиотеки
 */
public class FileManager {
    private static final String DATA_FILE = "library_data.txt";
    
    /**
     * Сохраняет информацию о книгах в файл
     */
    public void saveLibraryData(List<Book> books) throws IOException {
        try (FileWriter writer = new FileWriter(DATA_FILE);
             BufferedWriter bufferedWriter = new BufferedWriter(writer)) {
            
            for (Book book : books) {
                String line = String.format("%s|%s|%s|%d|%s",
                    book.getIsbn(),
                    book.getTitle(),
                    book.getAuthor(),
                    book.getYear(),
                    book.isAvailable());
                bufferedWriter.write(line);
                bufferedWriter.newLine();
            }
        }
    }
    
    /**
     * Загружает информацию о книгах из файла
     */
    public List<Book> loadLibraryData() throws IOException {
        List<Book> books = new ArrayList<>();
        File file = new File(DATA_FILE);
        
        if (!file.exists()) {
            return books;
        }
        
        try (FileReader reader = new FileReader(file);
             BufferedReader bufferedReader = new BufferedReader(reader)) {
            String line;
            
            while ((line = bufferedReader.readLine()) != null) {
                String[] parts = line.split("\\|");
                if (parts.length == 5) {
                    try {
                        Book book = new Book(
                            parts[0],
                            parts[1],
                            parts[2],
                            Integer.parseInt(parts[3])
                        );
                        book.setAvailable(Boolean.parseBoolean(parts[4]));
                        books.add(book);
                    } catch (NumberFormatException e) {
                        // Пропускаем строку с неверным форматом
                        System.err.println("Ошибка парсинга строки: " + line);
                    }
                }
            }
        }
        return books;
    }
    
    /**
     * Экспортирует логи в файл
     */
    public void exportLogs(List<String> logs, String filename) throws IOException {
        FileWriter writer = new FileWriter(filename);
        for (String log : logs) {
            writer.write(log + "\n");
        }
        writer.close();
    }
}

