from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from catalog.constants import (
    MAX_LENGTH_GENRE_NAME, MAX_LENGTH_BOOK_TITLE, MAX_LENGTH_AUTHOR_NAME,
    MAX_LENGTH_BOOK_SUMMARY, MAX_LENGTH_ISBN, MAX_LENGTH_BOOKINSTANCE_IMPRINT,
    MAX_LENGTH_BOOKINSTANCE_STATUS, LoanStatusEnum
)
import uuid

class Genre(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_GENRE_NAME,
        help_text=_("Enter a book genre (e.g. Science Fiction)")
    )

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=MAX_LENGTH_AUTHOR_NAME)
    last_name = models.CharField(max_length=MAX_LENGTH_AUTHOR_NAME)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(_('Died'), null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Book(models.Model):
    title = models.CharField(max_length=MAX_LENGTH_BOOK_TITLE)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=MAX_LENGTH_BOOK_SUMMARY)
    isbn = models.CharField(
        _('ISBN'),
        max_length=MAX_LENGTH_ISBN,
        unique=True,
        help_text=_('13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    )
    genre = models.ManyToManyField(Genre, help_text=_('Select a genre for this book'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'  # Đặt tên cột hiển thị trong Django Admin




class BookInstance(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text=_('Unique ID for this particular book across whole library')
    )
    book = models.ForeignKey('Book', on_delete=models.RESTRICT)
    imprint = models.CharField(max_length=MAX_LENGTH_BOOKINSTANCE_IMPRINT)
    due_back = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=MAX_LENGTH_BOOKINSTANCE_STATUS,
        choices=LoanStatusEnum.choices(),
        default=LoanStatusEnum.default(),
        help_text=_('Book availability')
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'
