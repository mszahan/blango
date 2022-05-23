# step 1 for logging
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blog.models import Post
from blog.forms import CommentForm

#for caching
# from django.views.decorators.cache import cache_page
# from django.views.decorators.vary import vary_on_cookie


# step2 for logging 
logger = logging.getLogger(__name__)


# @cache_page(300)
# @vary_on_cookie # this will change the chaching based on the cookie data cahnges that is the request.user
def index(request):
  # for checking the chaching flaws
    # from django.http import HttpResponse
    # return HttpResponse(str(request.user).encode("ascii"))

    # the select_related is for fetching multiple table data by joining them .....
    # So this will optimize the database than fetching data from multiple table simultaneously...
    # this tecnique reduces the number of query
    posts = Post.objects.filter(published_at__lte=timezone.now()).select_related("author")

    ## ...... this should not be used as it need constant update if new field is added to model...
    ## .. at the same time it does not speed up much...
    
    ## this only fetching the included column from the database table
    # posts = (
    # Post.objects.filter(published_at__lte=timezone.now())
    # .select_related("author")
    # .only("title", "summary", "content", "author", "published_at", "slug")
    # )

    # # this one does the similar task as previous....
    # # but this one rquires less code to fetch more data
    # posts = (
    # Post.objects.filter(published_at__lte=timezone.now())
    # .select_related("author")
    # .defer("created_at", "modified_at")
    # )


    
    # for loggin the number of posts added
    logger.debug("Got %d posts", len(posts))

    return render(request, "blog/index.html", {'posts':posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                # for loggin the comment
                logger.info(
                    "Created comment on Post %d for user %s", post.pk, request.user
                )

                # this is intersting never use request.path_info before
                # request.path_info keeps you in the same page
                # I have been looking for this.
                # I have implemeted this calling the absolute url before
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None


    return render(request, "blog/post-detail.html", {"post": post, "comment_form": comment_form})

# this view is to find out the ip address
def get_ip(request):
  from django.http import HttpResponse
  return HttpResponse(request.META['REMOTE_ADDR'])
