from django import forms   
from app.models import UserQuery   

class  UserQueryForm (forms.ModelForm):   
    class Meta:
        model = UserQuery
        fields = "__all__"
        widgets = {
            "question": forms.TextInput(attrs={
                "type":"text",
                "id": "chatInput",
                "class": "chat-input",
                "name": "question",
                "placeholder": "Ketik pertanyaan Anda...",
                "autocomplete": "off"
            })
        }