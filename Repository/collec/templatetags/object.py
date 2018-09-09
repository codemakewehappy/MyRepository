from django import template
from collec.models import Asset

register = template.Library()


class AssetNode(template.Node):
    def __init__(self, limit, varname):
        self.limit, self.varname = limit, varname

    def __repr__(self):
        return "<GetAdminLog Node>"

    def render(self, context):
        context[self.varname] = Asset.objects.all()[:int(self.limit)]
        return ''


@register.tag
def get_objects(parser, token):
    """
    Populates a template variable with the admin log for the given criteria.

    Usage::

        {% get_admin_log [limit] as [varname] for_user [context_var_containing_user_obj] %}

    Examples::

        {% get_admin_log 10 as admin_log for_user 23 %}
        {% get_admin_log 10 as admin_log for_user user %}
        {% get_admin_log 10 as admin_log %}

    Note that ``context_var_containing_user_obj`` can be a hard-coded integer
    (user ID) or the name of a template context variable containing the user
    object whose ID you want.
    """
    tokens = token.contents.split()

    return AssetNode(limit=tokens[1], varname=tokens[3])
