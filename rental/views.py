from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from .models import Book, BookCopy, Rental, RentalItem
from .forms import RegisterForm

# Homepage view
def home(request):
    books = Book.objects.all()
    return render(request, 'home.html', {'books': books})

# Book detail view
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    available_copies = book.bookcopy_set.filter(status='available')
    return render(request, 'book_detail.html', {
        'book': book,
        'available_copies': available_copies,
        'available_count': available_copies.count()
    })

# Rent a book
@login_required
def rent_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    available_copy = book.bookcopy_set.filter(status='available').first()

    if not available_copy:
        messages.error(request, 'No copies available for rent.')
        return redirect('book_detail', pk=pk)

    rental = Rental.objects.create(
        user=request.user,
        due_date=timezone.now() + timezone.timedelta(days=7)
    )

    RentalItem.objects.create(rental=rental, book_copy=available_copy)
    available_copy.status = 'rented'
    available_copy.save()

    messages.success(request, f'Successfully rented "{book.title}"!')
    return redirect('my_rentals')

# View user's rentals
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

# Return a book
@login_required
def return_book(request, rental_id):
    rental = get_object_or_404(Rental, pk=rental_id, user=request.user)

    if rental.status == 'returned':
        messages.warning(request, 'This book has already been returned.')
        return redirect('my_rentals')

    rental.status = 'returned'
    rental.returned_at = timezone.now()
    rental.save()

    for item in rental.rentalitem_set.all():
        item.book_copy.status = 'available'
        item.book_copy.save()

    messages.success(request, 'Book returned successfully!')
    return redirect('my_rentals')

# User registration
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