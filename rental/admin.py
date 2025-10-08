from django.contrib import admin
from .models import Book, BookCopy, Rental, RentalItem

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'created_at', 'available_copies_count')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('created_at',)

@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ('book', 'copy_number', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('book__title',)

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rented_at', 'due_date', 'status')
    list_filter = ('status', 'rented_at')
    search_fields = ('user__username',)

@admin.register(RentalItem)
class RentalItemAdmin(admin.ModelAdmin):
    list_display = ('rental', 'book_copy', 'created_at')
    search_fields = ('rental__id', 'book_copy__book__title')