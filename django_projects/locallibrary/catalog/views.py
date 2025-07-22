from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre



def index(request):
    """View function for home page of site."""

    # Đếm số lượng các đối tượng chính
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    # Đếm book instance có status = 'a' (available)
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # Đếm số tác giả
    num_authors = Author.objects.count()

    # Truyền dữ liệu vào template
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render trang index.html với dữ liệu context
    return render(request, 'catalog/index.html', context)
