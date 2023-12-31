from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from news.models import Author


@login_required
def set_author(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        Author.objects.create(user_id=user.id)
        author_group.user_set.add(user)

    return redirect('/account/')
