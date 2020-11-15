from django import forms
from django.utils.safestring import mark_safe

class RenewPostForm(forms.Form):

    # mark_safe() func →　new line func
    renewal_title = forms.CharField(help_text=mark_safe("(Enter a title that can enter up to 30 characters.)<br /><br />"))
    renewal_date = forms.DateField(help_text=mark_safe("(Enter a date that want. default : Current Date)<br /><br />"))
    renewal_description = forms.CharField(help_text=mark_safe("(Enter a description that can enter up to 500 characters.)<br />"))

    # Validation check of Post form
    #def clean_renewal_title(self):

    #def clean_renewal_date(self):

    #def clean_renewal_description(self):

class PostCreateForm(forms.Form):

    # mark_safe() func →　new line func
    create_title = forms.CharField(help_text=mark_safe("(Enter a title that can enter up to 30 characters.)<br /><br />"))
    create_description = forms.CharField(help_text=mark_safe("(Enter a description that can enter up to 500 characters.)<br />"))

    # Validation check of Post form
    #def clean_renewal_title(self):

    #def clean_renewal_date(self):

    #def clean_renewal_description(self):



class CommentCreateForm(forms.Form):

    create_description = forms.CharField(help_text=mark_safe("(Enter a description that can enter up to 500 characters.)<br />"))

class CommentUpdateForm(forms.Form):

    update_description = forms.CharField(help_text=mark_safe("(Enter a description that can enter up to 500 characters.)<br />"))

class CommentDeleteForm(forms.Form):

    delete_description = forms.CharField()
