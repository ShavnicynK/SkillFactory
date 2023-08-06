from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from datetime import timedelta
from django.utils import timezone
from .filters import PostFilter
from .forms import PostForm, CategoryForm
from .models import Post, Category, CategorySubscribers, Author


class PostList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostSearch(ListView):
    model = Post
    ordering = '-date'
    template_name = 'post_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['filter_on'] = True if len(self.filterset.data) else False
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        author = Author.objects.get(user_id=self.request.user.id)
        limit_time = timezone.now() - timedelta(days=1)
        count_post = Post.objects.filter(author_id=author.id, date__gte=limit_time).count()

        if count_post <= 5:
            post = form.save(commit=False)
            path = self.request.path
            post.author_id = Author.objects.filter(user_id=self.request.user.id).values('id')
            if path == '/articles/create/':
                post.type = 'A'
            return super().form_valid(form)
        else:
            messages.info(self.request, 'Хватит уже сегодня постить')
            return redirect('/news/')


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class CategoryList(ListView):
    model = Category
    ordering = 'name'
    template_name = 'categorys.html'
    context_object_name = 'categorys'
    paginate_by = 10


class CategoryBlog(DetailView):
    model = Category
    template_name = 'category_blog.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.id is not None:
            context['is_anonym'] = False
            context['is_subscribe'] = CategorySubscribers.objects.filter(user_id=user.id,
                                                                         category_id=Category.objects.get(
                                                                             name=kwargs['object'])).exists()
        else:
            context['is_anonym'] = True
            context['is_subscribe'] = False

        context['posts'] = Post.objects.filter(categorys__name=kwargs['object'])

        return context


class CategoryCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'category.add_category'
    model = Category
    form_class = CategoryForm
    template_name = 'category_edit.html'


def set_subscribe(request, pk):
    user = request.user
    if not CategorySubscribers.objects.filter(user_id=user.id, category_id=pk).exists():
        CategorySubscribers.objects.create(category_id=pk, user_id=user.id)
        messages.info(request, 'Вы успешно подписались на рассылку')
    else:
        messages.info(request, 'Вы уже подписались раньше')

    return redirect(request.META.get('HTTP_REFERER'))

