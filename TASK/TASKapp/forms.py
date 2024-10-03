from django import forms
from .models import *
from django import forms
from .models import Task  

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'status']  # 指定要使用的欄位

    title = forms.CharField(label='任務名稱', max_length=100)
    description = forms.CharField(label='描述', widget=forms.Textarea(attrs={'name': 'body'}))
    due_date = forms.DateTimeField(label='到期日', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),input_formats=['%Y-%m-%dT%H:%M'])
    priority = forms.IntegerField(label='優先權')

    status_choice = [
        ['待辦', '待辦'],
        ['進行中', '進行中'],
        ['完成', '完成']
    ]
    status = forms.ChoiceField(label='狀態', choices=status_choice)

class ShareForm(forms.Form):
    user = forms.CharField(label='使用者名稱', max_length=100)

class CommentForm(forms.Form):
    comment = forms.CharField(label='描述', widget=forms.Textarea(attrs={'name': 'body'}))