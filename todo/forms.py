from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('title', 'description', 'important')

        title = forms.CharField(label="제목")  # 'Title'을 '제목'으로 변경
        description = forms.CharField(label="내용")  # 'Description'을 '내용'으로 변경
        important = forms.BooleanField(label="중요도")  # 'Important'를 '중요도'로 변경
