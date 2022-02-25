from django import template

register = template.Library()

@register.filter()
def get_likes(self):
    return self.likes.count()