from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic

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
    

class BookListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Book
    paginate_by = 2

class BookDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Book
    def book_detail_view(request_key):
        try:
            book = Book.objects.get(pk=primary_key)
        except Book.DoesNotExist:
            raise Http404('Book does not exist')

        return render(request, 'catalog/book_detail.html', context={'book': book})

class AuthorListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Author



class AuthorDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = Author
