from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.utils import timezone
# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post
    # connect the model

    def get_queryset(self):
        # 6:00 use django orm when dealing with generic vies to add a custom touch to it
        # did this with function based views can define get methods for class based views too
        return Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')
        # 7:00 with a get_queryset we're basically doing a sql query on our model
        # this is basically the pthon version of writing a sql query
        # the above line of code says grab the post model and filter based on the conditions
        # with field querys you can say __ and then the field condition so lte is less than or equal to,
        # the rest of the code says grab the published_date that are less than or equal to the current time and then order them
        # by published_date but since we did a dash it will do descending order not ascending order or we would get the oldest
        # blog posts first

# 15:40 mixins are the class based views version of decorators that function based views had
# 16:40 they are basically classes we mix in with the classes we inherit with
class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    # 17:36 if the perosn isnt logged in they should go to the login_url which will be set up later
    # 17:50 they will then be redirected to redirect_field_name (i think)
    redirect_field_name = 'blog/post_detail.html'
    # we need the login_url as well as the redirect-field_name
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    # 17:36 if the perosn isnt logged in they should go to the login_url which will be set up later
    # 17:50 they will then be redirected to redirect_field_name (i think)
    redirect_field_name = 'blog/post_detail.html'
    # we need the login_url as well as the redirect-field_name
    form_class = PostForm
    model = Post

    # should look the same as create but instead we're just updating the post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
    # 23:40 the success url is basically after we delete the url where do we go
    # 23:30 when we are deleteing a view we dont want the success url to actually activate until we delete the view
    # in order to do this we use reverse lazy

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_draft_list.html'
    model = Post
    context_object_name = 'post_draft_list'
    template_name = 'post_draft_list.html'


    def get_queryset(self):
        return Post.objects.filter(published_date__isnull = True).order_by('created_date')
        # 28:25 if this is a list of my drafts i want to make sure i dont have a publication date
        # so i want isnull to be True

##############################################
##############################################
# function based views
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk = pk)
    post.publish()
    return redirect('post_detail', pk = pk)
    # 17:00 once we publish the post just go to the post_detail page where the primary key is the primary key
    # of the post we just made

@login_required
def add_comment_to_post(request, pk):
    # in order to create a comment you must be logged in
    # 7:50 and we take the request as well as the primary key that links the comment to the post
    # either get the  post object or send a 404 couldn't find the object
    post = get_object_or_404(Post, pk=pk)
    # if the request method == post then it means someone has filled out the form
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            # l169 8:30 commit = False means we have some sort of form in memory
            comment.post = post
            # l169 the explaination of comment.post = post is as follows
            # in models.py the comment object has a post attribute which is connected by a foreign key
            # to the post class
            # the above line basically says make the post = to that comment.post from above
            comment.save()
            # save the comment and once you're done redirect to the post_detail page with the primary key
            # being equal to post.pk which is just the primary key for the actual blog post
            return redirect('post_detail', pk=post.pk)
    # if the request method isn't post(so someone has not filled out the form then)
    else:
        form = CommentForm()
    # l169 9:15 return the comment_form.html and pass in the context dictionary
    # so when we go to the comment_form.html page we can inject the form dictionary
    return render(request, 'blog/comment_form.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    comment.approve()
    # this is coming from our approve method in the comment class in models.py
    # 12:00 the method just flips the approved_comment attribute to true
    return redirect('post_detail', pk=comment.post.pk)
    # 12:30 what is happening here basically  after approving the comment we may want to go to the post of that
    # comment then i need the post.pk so we check what the pk of the post the comment was linked to is

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk = post_pk)
    # 14:50 the reason this return on comment_approve's return is different is because we 
    # have an extra variable called post_pk this is important because we can't do what we did in
    # comment-approve as by the time we get to return we already deleted the comment so it doesn't remember what
    # the pk is  
