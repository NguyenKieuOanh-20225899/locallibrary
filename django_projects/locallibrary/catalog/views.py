from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.decorators import permission_required

import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from catalog.forms import RenewBookForm
from django.contrib.auth.mixins import PermissionRequiredMixin
def index(request):
    """View function for home page of site."""

    # Đếm số lượng các đối tượng chính
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    # Đếm book instance có status = 'a' (available)
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # Đếm số tác giả
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    # Truyền dữ liệu vào template
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render trang index.html với dữ liệu context
    return render(request, 'catalog/index.html', context)

class BookListView(generic.ListView):
    model = Book

    # Tuỳ chỉnh tên biến context (mặc định là book_list)
    #context_object_name = 'my_book_list'

    # Lọc dữ liệu, giới hạn số lượng
  
    paginate_by = 2
    # Tuỳ chỉnh đường dẫn template (không theo pattern mặc định nữa)
    template_name =  'catalog/book_list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

class BookDetailView(generic.DetailView):
    model = Book

@permission_required('catalog.can_mark_returned')
@permission_required('catalog.can_edit')  # ví dụ thêm
class MyView(LoginRequiredMixin, View):
    login_url = '/login/'  # Đường dẫn trang đăng nhập thay vì mặc định /accounts/login/
    redirect_field_name = 'redirect_to'  # Dùng ?redirect_to=/duong-dan-thay-vi-next
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user
        ).filter(status__exact='o').order_by('due_back')
@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def return_book(request, pk):
    """View function to return a borrowed book (by changing status to available)."""
    book_instance = get_object_or_404(BookInstance, pk=pk)
    book_instance.status = 'a'  # Mark as available
    book_instance.borrower = None
    book_instance.due_back = None
    book_instance.save()
    return HttpResponseRedirect(reverse('my-borrowed'))
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            # Ghi ngày mới vào trường due_back
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('all-borrowed'))

    else:
        # Nếu GET: hiển thị form với ngày mặc định là 3 tuần từ hôm nay
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__'  
class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')  
from django.views.generic import DetailView

class AuthorDetail(DetailView):
    model = Author

class AuthorListView(generic.ListView):
    model = Author
    template_name = 'catalog/author_list.html'
    paginate_by = 10

@classmethod
def setUpTestData(cls):
    number_of_authors = 13
    for author_num in range(number_of_authors):
        Author.objects.create(
            first_name=f'Author{author_num}',
            last_name=f'Surname{author_num}',
        )
