from django.shortcuts import render, get_object_or_404
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookForm

@login_required
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # Если данный запрос типа POST, тогда
    if request.method == 'POST':

        # Создаем экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = RenewBookForm(request.POST)

        # Проверка валидности данных формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data 
            #(здесь мы просто присваиваем их полю due_back)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # Переход по адресу 'all-borrowed':
            return HttpResponseRedirect(reverse('all-borrowed') )

    # Если это GET (или какой-либо еще), создать форму по умолчанию.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

@login_required
def index(request):
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    
    context = {
    'num_books':num_books,
    'num_instances':num_instances,
    'num_instances_available':num_instances_available,
    'num_authors':num_authors, 
    'num_visits':num_visits}

    return render(request, 'catalog/index.html', context=context)
    

class BookListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view for a list of books."""
    model = Book
    paginate_by = 2

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Book
    def book_detail_view(request_key):
        try:
            book = Book.objects.get(pk=primary_key)
        except Book.DoesNotExist:
            raise Http404('Book does not exist')

        return render(request, 'catalog/book_detail.html', context={'book': book})

class AuthorListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Author



class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    """Generic class-based detail view for an author."""
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user. 
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')