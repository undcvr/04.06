from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _



class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(verbose_name=_('Заголовок'), max_length=100)
    author = models.CharField(verbose_name=_('Автор'), max_length=100)
    is_available = models.BooleanField(_('В доступе'), default=True)

    class Meta:
        verbose_name = _('Книга')
        verbose_name_plural = _('Книги')

    def __str__(self) -> str:
        return f'{self.title} by {self.author}'


class BorrowedBook(models.Model):
    book = models.ForeignKey(
        verbose_name=_('Книга'),
        to=Book,
        on_delete=models.CASCADE,
        related_name='borrowed_book',
    )
    borrower = models.ForeignKey(
        verbose_name=_('Забронирована'),
        to=User,
        on_delete=models.CASCADE,
        related_name='borrowed_book',
    )
    date_borrowed = models.DateTimeField(
        verbose_name=_('Дата брони'), auto_now_add=True
    )
    date_returned = models.DateTimeField(_('Дата возврата'), null=True, blank=True)

    class Meta:
        verbose_name = _('Забронированная книга')
        verbose_name_plural = _('Забронированные книги')

    def __str__(self) -> str:
        return f'{self.book} by {self.borrower}'
