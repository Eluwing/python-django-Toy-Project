import datetime, sys

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.utils import timezone

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

# Generic Editing Views related API
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.
from dryblog.models import Post, Comment
from dryblog.forms import RenewPostForm, CommentCreateForm, CommentUpdateForm, CommentDeleteForm, PostCreateForm

def index(request):
    """View function for home page of site."""

    #confirm the user has administrator permission
    blog_admin_flag = admin_permissions_confirm(request)


    # Generate counts of some of the main objects
    num_posts = Post.objects.all().count()
    num_comments = Comment.objects.all().count()

    # # Available books (status = 'a')
    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # # The 'all()' is implied by default.
    # num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_posts': num_posts,
        'num_comments': num_comments,
        'num_visits': num_visits,
        'blog_admin_flag' : blog_admin_flag,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class PostListView(generic.ListView):
    model = Post
    paginate_by = 5


    def get_context_data(self, **kwargs):

        post_obj_all = Post.objects.all()
        login_id = self.request.user.username
        context = super().get_context_data(**kwargs)
        true_title_list = []
        blog_admin_flag = False

        blog_admin_flag = admin_permissions_confirm(self.request)

        temp = Session.objects.filter(expire_date__gte=timezone.now())


        print("Connected Session user  : "+str(temp), file=sys.stderr)

        # Select users who can crud
        for post_obj in post_obj_all :
            if post_obj.p_name == login_id :

                true_title_list.append(post_obj.p_title)


        context['true_title_list'] = true_title_list
        context['blog_admin_flag'] = blog_admin_flag

        return context

class PostDetailView(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):

        blog_admin_flag = admin_permissions_confirm(self.request)

        context = super().get_context_data(**kwargs)
        context['blog_admin_flag'] = blog_admin_flag
        return context

#해당 세션 유저만 가능하게 해야함
#로그인한 유저만
#@permission_required('dryblog.can_crud')
@login_required
def renew_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    #Allowed if you are the posted
    crud_flag = crud_permissions(request.user.username, post.p_name)
    blog_admin_flag = admin_permissions_confirm(request)

    #if user have not blog admin permission and crud permission
    if crud_flag == False and blog_admin_flag == False :

        return HttpResponseRedirect(reverse('post'))




    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewPostForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            post.p_title = form.cleaned_data['renewal_title']
            post.p_date = form.cleaned_data['renewal_date']
            post.p_description = form.cleaned_data['renewal_description']

            post.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('post'))

    # If this is a GET (or any other method) create the default form.
    else:
        #defalut date field : current time

        proposed_renewal_date = datetime.date.today()

        form = RenewPostForm(
            initial= {

                'renewal_date': proposed_renewal_date,

        })

    context = {
        'form': form,
        'post': post,
        'blog_admin_flag' : blog_admin_flag,

    }

    return render(request, 'dryblog/renew_post.html', context)

class PostCreate(CreateView):
    model = Post
    fields = '__all__'
    initial = {

        'p_date': datetime.date.today()

    }

    def get_context_data(self, **kwargs):

        blog_admin_flag = admin_permissions_confirm(self.request)

        context = super().get_context_data(**kwargs)
        context['blog_admin_flag'] = blog_admin_flag
        return context

@login_required
def post_create(request):

    form = PostCreateForm(request.POST)
    blog_admin_flag = admin_permissions_confirm(request)

    #if 'POST' request
    if request.method == 'POST':

        form = PostCreateForm(request.POST)

        if form.is_valid():

            in_create_title = form.cleaned_data['create_title']
            in_create_description = form.cleaned_data['create_description']

            create_post = Post(
                p_title = in_create_title,
                p_name = request.user.username,
                p_date = datetime.date.today(),
                p_description = in_create_description,
            )

            create_post.save()

            # redirect to 'post-detail' that 'blog/blogs/'
            return HttpResponseRedirect(reverse('post'))


    #if 'GET' request
    else:

        form = PostCreateForm()

    context = {
        'form': form,
        'blog_admin_flag': blog_admin_flag,
    }

    return render(request, 'dryblog/post_form.html', context)


# @login_required
class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('post')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        # self.object = self.get_object()
        # print(self.get_object(), file=sys.stderr)

        blog_admin_flag = admin_permissions_confirm(self.request)

        context['blog_admin_flag'] = blog_admin_flag
        return context

    #def get(self, request, pk) same as
    def get(self, request, *agrs, **kwargs):

        post = self.get_object()
        crud_flag = crud_permissions(self.request.user.username, post.p_name)
        blog_admin_flag = admin_permissions_confirm(self.request)

        # print("post : "+str(post), file=sys.stderr)
        # print("crud_flag : "+str(crud_flag), file=sys.stderr)
        # print("blog_admin_flag : "+str(blog_admin_flag), file=sys.stderr)

        if crud_flag == False and blog_admin_flag == False :

            # messages.warning(request, 'You have not permission for Post Delete')

            return render(request, 'dryblog/error_page.html')

        else :

            context = {
                'post' : post,
            }
            return render(request, 'dryblog/post_confirm_delete.html', context)

    def post(self, *args , **kwargs):

        post = self.get_object()
        crud_flag = crud_permissions(self.request.user.username, post.p_name)
        blog_admin_flag = admin_permissions_confirm(self.request)

        # print("post : "+str(post), file=sys.stderr)
        # print("crud_flag : "+str(crud_flag), file=sys.stderr)
        # print("blog_admin_flag : "+str(blog_admin_flag), file=sys.stderr)

        if crud_flag == False and blog_admin_flag == False :

            return HttpResponseRedirect(reverse('post'))

        else :

            post.delete()

        return HttpResponseRedirect(reverse('post'))


# comment Create, Update, Delete by Generic

@login_required
class CommentCreate(CreateView):
    model = Comment
    fields = '__all__'
    initial = {'c_date': datetime.date.today()}

@login_required
class CommentUpdate(UpdateView):
    model = Comment
    fields = ['c_description']

@login_required
class CommentDelete(DeleteView):
    model = Comment
    success_url = reverse_lazy('post')

# comment Create, Update, Delete by function
@login_required
def comment_create(request, post_id):

    post = get_object_or_404(Post, id = post_id)
    form = CommentCreateForm(request.POST)
    blog_admin_flag = admin_permissions_confirm(request)

    #if 'POST' request
    if request.method == 'POST':

        form = CommentCreateForm(request.POST)

        if form.is_valid():

            in_create_description = form.cleaned_data['create_description']

            create_comment = Comment(
                post = post,
                c_name = request.user.username,
                c_date = datetime.date.today(),
                c_description = in_create_description,
            )

            create_comment.save()

            # redirect to 'post-detail' that 'blog/blogs/'
            return HttpResponseRedirect(reverse('post'))


    #if 'GET' request
    else:

        form = CommentCreateForm()

    context = {
        'form': form,
        'blog_admin_flag': blog_admin_flag,
    }

    return render(request, 'dryblog/post_form.html', context)

@login_required
def comment_update(request, post_id, comment_id):

    obj_comment = get_object_or_404(Comment, id = comment_id)
    post = get_object_or_404(Post, id = post_id)
    form = CommentUpdateForm(request.POST)
    crud_flag = crud_permissions(request.user.username, obj_comment.c_name)
    blog_admin_flag = admin_permissions_confirm(request)

    #if user have not blog admin permission and crud permission
    if crud_flag == False and blog_admin_flag == False :

        return HttpResponseRedirect(reverse('post'))

    #if 'POST' request
    if request.method == 'POST':

        form = CommentUpdateForm(request.POST)

        if form.is_valid():

            comment_description = form.cleaned_data['update_description']

            update_comment = Comment(id = comment_id, post = post, c_description=comment_description)
            update_comment.save()

            # redirect to 'post-detail' that 'blog/blogs/post_id'
            return HttpResponseRedirect(reverse('post-detail', args=[post_id]))


    #if 'GET' request
    else:

        form = CommentUpdateForm(
            initial= {

                'update_description': '',

            })


    context = {
        'form': form,
        'post': post,
        'blog_admin_flag': blog_admin_flag,
    }

    return render(request, 'dryblog/comment_detail.html', context)

@login_required
def comment_delete(request, post_id, comment_id):

    obj_comment = get_object_or_404(Comment, id = comment_id)
    crud_flag = crud_permissions(request.user.username, obj_comment.c_name)
    blog_admin_flag = admin_permissions_confirm(request)

    #if user have not blog admin permission and crud permission
    if crud_flag == False and blog_admin_flag == False :

        return HttpResponseRedirect(reverse('post'))

    #if 'POST' request
    if request.method == 'POST':

        #Delete called comments
        obj_comment.delete();

        # redirect to 'post-detail' that 'blog/blogs/post_id'
        return HttpResponseRedirect(reverse('post-detail', args=[post_id]))


    #if 'GET' request
    else:
        delete_description = obj_comment.c_description

        context = {

            'delete_description' : delete_description,
            'blog_admin_flag ' : blog_admin_flag,
        }

        return render(request, 'dryblog/comment_delete_confirm.html',context)

    return HttpResponseRedirect(reverse('post-detail', args=[post_id]))

def user_detail(request, user_name) :

    user = User.objects.get(username = user_name)
    blog_admin_flag = admin_permissions_confirm(request)

    #if 'POST' request
    if request.method == 'GET':

        context = {

            'user' : user,
            'blog_admin_flag' : blog_admin_flag,

        }
        # redirect to 'post-detail' that 'blog/blogs/post_id'
        return render(request, 'dryblog/user_detail.html', context)




    #if 'POST' request
    else:



        return HttpResponseRedirect(reverse('post'))

    return HttpResponseRedirect(reverse('post'))

@login_required
def user_list(request) :

    user = User.objects.all()
    blog_admin_flag = admin_permissions_confirm(request)

    #print(user, file=sys.stderr)
    print(request.user.groups, file=sys.stderr)
    #if 'POST' request
    if request.method == 'GET':

        context = {

            'obj_user' : user,
            'blog_admin_flag' : blog_admin_flag,

        }
        # redirect to 'post-detail' that 'blog/blogs/post_id'
        return render(request, 'dryblog/user_list.html', context)


    #if 'POST' request
    else:



        return HttpResponseRedirect(reverse('post'))

    return HttpResponseRedirect(reverse('post'))

def crud_permissions(request_get_name, post_get_name):

    if request_get_name == post_get_name:
        return True
    else :
        return False

def admin_permissions_confirm(obj_request):

    user_perm_list = str(obj_request.user.get_group_permissions())
    admin_perm_flag = False

    if "auth.change_user" in user_perm_list :
        admin_perm_flag = True

    return admin_perm_flag
