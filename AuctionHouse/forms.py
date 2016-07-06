# -*-coding:utf-8-*-

from django.forms import *
from .models import *
class RegisterUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['user_name', 'password', 'email', 'phone']
        labels = {'user_name': '用户名',
                  'password': '密码',
                  'email': '邮箱',
                  'phone': '手机'}
        widgets = {'password': PasswordInput}

class LoginUserForm(Form):
    name_or_email = CharField(label='用户名/邮箱', max_length=30)
    password = CharField(label='密码', max_length=30, widget=PasswordInput)


class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['password', 'email', 'phone', 'real_name', 'real_id',
                  'gender', 'portrait', 'birthday']
        labels = {'user_name': '用户名',
                  'password': '密码',
                  'email': '邮箱',
                  'phone': '手机',
                  'real_name': '真实姓名',
                  'real_id': '证件号码',
                  'gender': '性别',
                  'portrait': '头像',
                  'birthday': '生日'}
        widgets = {'password': PasswordInput}
#
# class UserForm(forms.Form):
#     user_name = forms.CharField(label='用户名', max_length=30)
#     password = forms.CharField(label='密码', max_length=36)
#     email = forms.EmailField(label='电子邮件')
#     real_name = forms.CharField(label='真实姓名', max_length=30)
#     real_id = forms.CharField(label='证件号码', max_length=30)
#     phone = forms.CharField(label='手机号', max_length=30)
#
#

#
#
# class ShowUserForm(forms.Form):
#     user_name = forms.CharField(label='用户名', max_length=30)
#     password = forms.CharField(label='密码', max_length=36)
#     email = forms.EmailField(label='电子邮件')
#     real_name = forms.CharField(label='真实姓名', max_length=30)
#     real_id = forms.CharField(label='证件号码', max_length=30)
#     phone = forms.CharField(label='手机号', max_length=30)
#     # 性别，默认为男
#     MALE = 'M'
#     FEMALE = 'F'
#     GENDER = (
#         (MALE, 'Male'),
#         (FEMALE, 'Female'),
#     )
#     gender = forms.ChoiceField(widget=forms.RadioSelect, choices=GENDER)
#     # gender = forms.CharField(max_length=2)
#     portrait = forms.ImageField(widget=forms.ClearableFileInput)
#     birthday = forms.DateField(required=False, widget=forms.SplitDateTimeWidget)
#     # 信用等级
#     credit = forms.FloatField(required=False)

class UploadGoodsForm(ModelForm):
    class Meta:
        model = Goods
        fields = ['goods_name', 'remaining_number', 'description', 'start_bid', 'buy_it_now_price', 'image_description']
        labels = {'goods_name': '商品名',
                  'remaining_number': '数量',
                  'description': '描述',
                  'start_bid': '起拍价',
                  'buy_it_now_price': '一口价',
                  'image_description': '上传图片'}
        widgets = {'description': Textarea(attrs={'cols': 60, 'rows': 8})}

class AddressForm(ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = ['delivery_name', 'delivery_phone', 'address', 'postcode']
        labels = {'delivery_name': '收件人名',
                  'delivery_phone': '联系电话',
                  'address': '详细地址',
                  'postcode': '邮编',}
