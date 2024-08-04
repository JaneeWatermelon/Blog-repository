from django import template

register = template.Library()

@register.filter
def my_int(value):
    if value >= 1000000000:
        return f'{round(value/1000000000, 1)} b'
    elif value >= 1000000:
        return f'{round(value / 1000000, 1)} m'
    elif value >= 1000:
        return f'{round(value / 1000, 1)} t'
    else:
        return value

@register.filter
def is_star(obj, user):
    if obj.id in user.star_categories_id:
        return True
    else:
        return False

@register.filter
def is_zero_star(user):
    if 0 in user.star_categories_id:
        return True
    else:
        return False

@register.filter
def is_heart(obj, user):
    if obj.id in user.liked_news_id:
        return True
    else:
        return False

@register.filter
def is_liked(obj, user):
    if obj.id in user.liked_comments_id:
        return True
    else:
        return False
@register.filter
def is_disliked(obj, user):
    if obj.id in user.disliked_comments_id:
        return True
    else:
        return False

