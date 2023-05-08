from django import forms
from blog.models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        # 2:20 connect to the model we are using
        fields = ('author', 'title', 'text')
        # 2:41 connect the fields we want to be able to edit in this form

        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs = {'class':'editable medium-editor-textarea postcontent '})
            # 6:00 the long class name will be explained later but the postcontent is our class name
            # we're connecting our text area attribute to  three css classes
            # the editable medium-editor which is the editable class which means we can edit it
            # the medium-editor-textarea which gives the styling of the actual medium editor
            # post content is our own class
            # 6:40 we do the same thing for title but say its textinputclass which is our own class as well
        }


class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'author':forms.TextInput(attrs = {'class': 'textinputclass'}),
            'text':forms.Textarea(attrs = {'class':'editable medium-editor-textarea'})
        }
        # 8:00 the general overview of how to link specific widgets to css styling
        # you have widgets which is a dictionary attribute inside of the meta class, you have the actual field, 
        # you'll see forms.actual widget its' going to be, and then you set attributes where you have a class key and
        # then the name of the class that eventually will go inside your css