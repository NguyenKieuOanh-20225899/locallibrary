import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text="Enter a date between now and 4 weeks (default 3)."
    )

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # 1. Ngày không được ở quá khứ
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # 2. Ngày không được vượt quá 4 tuần từ hôm nay
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # 3. Trả lại dữ liệu hợp lệ
        return data
