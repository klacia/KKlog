from KKlog.blog.models import Post, Comment
from calendar import month_name
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.db import connection
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
import time


"""-------------------"""
""" URL view function """
"""-------------------"""

def main(request):
    """Main listing."""
    posts_list = Post.objects.all().order_by("-published")
    posts = paginator(request,posts_list)
    print connection.queries
    return render_to_response("blog/list.html", dict(posts=posts, user=request.user, months=mkmonth_lst()))

def month(request, year, month):
    """Monthly archive."""
    posts_list = Post.objects.filter(published__year=year, published__month=month)
    posts = paginator(request,posts_list)
    print connection.queries
    return render_to_response("blog/list.html", dict(posts=posts, user=request.user,
                                                months=mkmonth_lst(), archive=True))
    
def post(request, pk):
    """Single post with comments and a comment form."""
    post = Post.objects.get(pk=int(pk))
    comments = Comment.objects.filter(post=post)
    d = dict(post=post, comments=comments, form=CommentForm(), user=request.user, months=mkmonth_lst(),)
    d.update(csrf(request))
    print connection.queries
    return render_to_response("blog/post.html", d)

"""----------------------"""
""" View utils functions """
"""----------------------"""

def paginator(request, posts_list):
    paginator = Paginator(posts_list, 2)
    
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)
    
    return posts

def mkmonth_lst():
    """Make a list of months to show archive links."""

    if not Post.objects.count(): return []

    # set up vars
    year, month = time.localtime()[:2]
    first = Post.objects.order_by("published")[0]
    fyear = first.published.year
    fmonth = first.published.month
    months = []

    # loop over years and months
    for y in range(year, fyear-1, -1):
        start, end = 12, 0
        if y == year: start = month
        if y == fyear: end = fmonth-1

        for m in range(start, end, -1):
            months.append((y, m, month_name[m]))
    return months

"""------------------"""
"""  View form stuff """
"""------------------"""

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]
    
def add_comment(request, post_pk):
    """Add a new comment."""
    p = request.POST

    if p.has_key("body") and p["body"]:
        author = "Anonymous"
        if p["author"]: author = p["author"]

        comment = Comment(post=Post.objects.get(pk=post_pk))
        cf = CommentForm(p, instance=comment)
        cf.fields["author"].required = False

        comment = cf.save(commit=False)
        comment.author = author
        comment.save()
    print connection.queries
    return HttpResponseRedirect(reverse("KKlog.blog.views.post", args=[post_pk]))
    
def delete_comment(request, post_pk, comment_pk=None):
    """Delete comment(s) with primary key `comment_pk` or with pks in POST."""
    if request.user.is_staff:
        if not comment_pk: pklst = request.POST.getlist("delete")
        else: pklst = [comment_pk]

        for pk in pklst:
            Comment.objects.get(pk=pk).delete()
    
    print connection.queries
    return HttpResponseRedirect(reverse("KKlog.blog.views.post", args=[post_pk]))