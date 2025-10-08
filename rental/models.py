from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=50, unique=True)
    cover = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def available_copies_count(self):
        return self.bookcopy_set.filter(status=1).count()

    def has_available_copies(self):
        return self.available_copies_count() > 0

class BookCopy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    copy_number = models.IntegerField()
    status = models.IntegerField(default=1, choices=[(1, 'Available'), (0, 'Rented')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Book Copies"
        unique_together = ('book', 'copy_number')

    def __str__(self):
        return f"{self.book.title} - Copy #{self.copy_number}"

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rented_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    returned_at = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(default=1, choices=[(1, 'Active'), (0, 'Returned')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rental #{self.id} - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = timezone.now() + timedelta(days=14)
        super().save(*args, **kwargs)

class RentalItem(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rental} - {self.book_copy}"