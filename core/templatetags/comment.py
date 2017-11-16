from blogs.models import Blog, Comment
from django import template

from django.db.models import Case, IntegerField, Q, When
from django.shortcuts import get_object_or_404

register = template.Library()


@register.inclusion_tag('blogs/show_comment.html', takes_context=True)
def show_comment(context, id):
    """Show comments"""
    q = Q(status='1normal')
    comments = Comment.objects.filter(post_id=id).filter(q).annotate(
        custom_order=Case(
            When(comment_id=0, then='id'),
            default='comment_id',
            output_field=IntegerField(),
        )
    ).order_by('custom_order', 'id')
    user = context['request'].user
    post = get_object_or_404(Blog, pk=id)

    return {
        'user': user,
        'post_user': post.user.username,
        'comments': comments,
        'count': comments.count()
    }
