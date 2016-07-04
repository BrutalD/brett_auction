# -*-coding:utf-8-*-

from django import forms

class UserForm(forms.Form):
    user_name = forms.CharField(label='用户名', max_length=30)
    password = forms.CharField(label='密码', max_length=36)
    email = forms.EmailField(label='电子邮件')
    real_name = forms.CharField(label='真实姓名', max_length=30)
    real_id = forms.CharField(label='证件号码', max_length=30)
    phone = forms.CharField(label='手机号', max_length=30)


class LoginUserForm(forms.Form):
    name_or_email = forms.CharField(label='用户名/邮箱', max_length=30)
    password = forms.CharField(label='密码', max_length=30)
