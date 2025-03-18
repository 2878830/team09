# encoding: utf-8
import re

from django import forms
from operation.models import UserAsk



# 进阶版本的modelform：它可以向model一样save  the smart modelform
class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    # 手机号的正则表达式验证 telephone number format
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"Illegal telephone number", code="mobile_invalid")
