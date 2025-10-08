from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    cover = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def available_copies_count(self):
        return self.bookcopy_set.filter(status='available').count()

    def __str__(self):
        return f"{self.title} by {self.author}"


class BookCopy(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'Maintenance'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    copy_number = models.PositiveIntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Copy {self.copy_number} of {self.book.title}"


class Rental(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rented_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')
    returned_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Rental #{self.id} by {self.user.username}"


class RentalItem(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book_copy} in Rental #{self.rental.id}"