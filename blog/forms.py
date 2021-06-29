from django.forms.models import fields_for_model
from .models import Follow, Post, Tag
from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model

non_allowed_usernames = ['abc']
# check for unique email & username

User = get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password"
            }
        )
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-confirm-password"
            }
        )
    )
    birth_date = forms.CharField(widget=forms.widgets.DateTimeInput(attrs={"type": "date"}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        print(cleaned_data.get('birth_date'))

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)
        if username in non_allowed_usernames:
            raise forms.ValidationError("This is an invalid username, please pick another.")
        if qs.exists():
            raise forms.ValidationError("This is an invalid username, please pick another.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError("This email is already in use.")
        return email



class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
        "class": "form-control"
    }))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password"
            }
        )
    )
    # def clean(self):
    #     data = super().clean()
    #     username = data.get("username")
    #     password = data.get("password")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username) # thisIsMyUsername == thisismyusername
        if not qs.exists():
            raise forms.ValidationError("This is an invalid user.")
        if qs.count() != 1:
            raise forms.ValidationError("This is an invalid user.")
        return username



class FollowForm(ModelForm):
    def __init__(self, exclude_list , *args,**kwargs):
        super(FollowForm, self).__init__(*args, **kwargs)
        self.fields['following_user'].queryset = User.objects.exclude(id__in = exclude_list)
    
    class Meta:
        model = Follow
        exclude = ('follower_user',)


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('context','tag')
    
    # def save(self):
    #     instance = forms.ModelForm.save(self)
    #     instance.post_set.clear()
    #     instance.post_set.add(*self.cleaned_data['tag'])
    #     return instance

class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)