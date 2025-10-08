from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.utils import timezone
from .models import Book, BookCopy, Rental, RentalItem
from .forms import BookForm, RegisterForm

def home(request):
    books = Book.objects.filter(bookcopy__status=1).distinct()
    return render(request, 'home.html', {'books': books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    available_copies = book.bookcopy_set.filter(status=1)
    return render(request, 'book_detail.html', {
        'book': book,
        'available_copies': available_copies,
        'available_count': available_copies.count()
    })

@login_required
def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            # Create 3 copies by default
            for i in range(1, 4):
                BookCopy.objects.create(book=book, copy_number=i)
            messages.success(request, 'Book added successfully with 3 copies!')
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'book_form.html', {'form': form, 'title': 'Add New Book'})

@login_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_detail', pk=pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'book_form.html', {'form': form, 'title': 'Edit Book', 'book': book})

@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('home')
    return render(request, 'book_delete.html', {'book': book})

@login_required
def rent_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    available_copy = book.bookcopy_set.filter(status=1).first()
    
    if not available_copy:
        messages.error(request, 'No copies available for rent.')
        return redirect('book_detail', pk=pk)
    
    # Create rental
    rental = Rental.objects.create(user=request.user)
    
    # Create rental item
    RentalItem.objects.create(rental=rental, book_copy=available_copy)
    
    # Update copy status
    available_copy.status = 0
    available_copy.save()
    
    messages.success(request, f'Successfully rented "{book.title}"!')
    return redirect('my_rentals')

@login_required
def my_rentals(request):
    rentals = Rental.objects.filter(user=request.user).order_by('-rented_at')
    rental_data = []
    
    for rental in rentals:
        items = rental.rentalitem_set.all()
        for item in items:
            rental_data.append({
                'rental': rental,
                'book': item.book_copy.book,
                'copy_number': item.book_copy.copy_number,
                'book_copy': item.book_copy,
            })
    
    return render(request, 'rentals.html', {'rental_data': rental_data})

@login_required
def return_book(request, rental_id):
    rental = get_object_or_404(Rental, pk=rental_id, user=request.user)
    
    if rental.status == 0:
        messages.warning(request, 'This book has already been returned.')
        return redirect('my_rentals')
    
    # Update rental status
    rental.status = 0
    rental.returned_at = timezone.now()
    rental.save()
    
    # Update all book copies in this rental
    for item in rental.rentalitem_set.all():
        item.book_copy.status = 1
        item.book_copy.save()
    
    messages.success(request, 'Book returned successfully!')
    return redirect('my_rentals')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
