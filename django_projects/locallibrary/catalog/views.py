from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.decorators import permission_required


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