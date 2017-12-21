from django import forms


#表单
class CustomersregistForm(forms.Form):
    name = forms.CharField(label='用户名',required=True,max_length=10)
    address = forms.CharField(label='地址',required=True,max_length=50)
    telephone = forms.CharField(label='联系电话',required=True,max_length=15)
    email = forms.EmailField(label='电子邮箱',required=True)
    password = forms.CharField(label='密码', required=True, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='密码', required=True, widget=forms.PasswordInput())

class CustomersForm(forms.Form):
    name = forms.CharField(label='用户名', required=True, max_length=10)
    password = forms.CharField(label='密码', required=True, widget=forms.PasswordInput())

class ManagersForm(forms.Form):   #其实这个定义并没有用。。。。
    name = forms.CharField(label='用户名', required=True, max_length=10)
    password = forms.CharField(label='密码', required=True, widget=forms.PasswordInput())