from django import forms
from .models import LiftProfile, LiftRecord, LiftPost, Comment


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = LiftProfile
        fields = ['first_name', 'last_name', 'city', 'email', 'profile_picture']

# Form to create a new lift record
class LiftRecordForm(forms.ModelForm):
    class Meta:
        model = LiftRecord
        fields = ['lift_type', 'weight', 'date_recorded']


# Form to create a new lift post
class LiftPostForm(forms.ModelForm):
    class Meta:
        model = LiftPost
        fields = ['caption', 'lift_record', 'image']  
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)
        if user:
            # Filter the queryset for 'lift_record' to include only the user's records
            self.fields['lift_record'].queryset = LiftRecord.objects.filter(user__user=user)



# Form to add a comment on a post
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
