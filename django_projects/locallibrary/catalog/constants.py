from django.utils.translation import gettext_lazy as _
from enum import Enum

# ================================
# General Constants
# ================================
MAX_LENGTH_GENRE_NAME = 200
MAX_LENGTH_ISBN = 13
MAX_LENGTH_AUTHOR_NAME = 100
MAX_LENGTH_BOOK_TITLE = 200
MAX_LENGTH_BOOK_SUMMARY = 1000
MAX_LENGTH_BOOKINSTANCE_STATUS = 1
MAX_LENGTH_BOOKINSTANCE_IMPRINT = 200

# ================================
# Book Loan Status Enum
# ================================
class LoanStatusEnum(Enum):
    MAINTENANCE = ('m', _('Maintenance'))
    ON_LOAN = ('o', _('On loan'))
    AVAILABLE = ('a', _('Available'))
    RESERVED = ('r', _('Reserved'))

    @classmethod
    def choices(cls):
        return [x.value for x in cls]

    @classmethod
    def default(cls):
        return cls.MAINTENANCE.value[0]
