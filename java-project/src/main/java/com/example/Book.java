package com.example;

/**
 * Класс, представляющий книгу в библиотеке
 */
public class Book {
    private String isbn;
    private String title;
    private String author;
    private int year;
    private boolean isAvailable;
    
    public Book(String isbn, String title, String author, int year) {
        this.isbn = isbn;
        this.title = title;
        this.author = author;
        this.year = year;
        this.isAvailable = true;
    }
    
    public String getIsbn() {
        return isbn;
    }
    
    public String getTitle() {
        return title;
    }
    
    public String getAuthor() {
        return author;
    }
    
    public int getYear() {
        return year;
    }
    
    public boolean isAvailable() {
        return isAvailable;
    }
    
    public void setAvailable(boolean available) {
        isAvailable = available;
    }
    
    @Override
    public String toString() {
        return String.format("%s - %s (%d) [ISBN: %s]", 
            author, title, year, isbn);
    }
}

