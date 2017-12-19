from django import forms
import json

#表单
class customersForm(forms.Form):
    name = forms.CharField(label='用户名',required=True,max_length=10)
    address = forms.CharField(label='地址',required=True,max_length=50)
    telephone = forms.CharField(label='联系电话',required=True,max_length=15)
    email = forms.EmailField(label='电子邮箱',required=True)
    password = forms.CharField(label='密码', required=True, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='密码', required=True, widget=forms.PasswordInput())

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password", False)
        confirm_password = self.cleaned_data["confirm_password"]
        if not (password == confirm_password):
 #           fail = {"info": "confirm_password and password are different"}
            raise forms.ValidationError("confirm_password and password are different")
        return confirm_password

class managersForm(forms.Form):
    name = forms.CharField(label='用户名', required=True, max_length=10)
    password = forms.CharField(label='密码', required=True, widget=forms.PasswordInput())