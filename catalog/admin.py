from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language


#admin.site.register(Author)
#admin.site.register(BookInstance)
#admin.site.register(Genre)
#admin.site.register(Language)

admin.site.register(Genre)
admin.site.register(Language)


# Register the admin class with the associated model
# Register the Admin classes for Book using the decorator

class BooksInline(admin.TabularInline):
    """Defines format of inline book insertion (used in AuthorAdmin)"""
    model = Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

class BooksInstanceInline(admin.TabularInline):
    list_filter = ('status', 'due_back')
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]
    
admin.site.unregister(Author)
admin.site.register(Author, AuthorAdmin)



# Register the Admin classes for BookInstance using the decorator

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
	list_display = ('book', 'status', 'due_back', 'id')
	list_filter = ['status', 'due_back']

	fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )



