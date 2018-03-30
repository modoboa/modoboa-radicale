"""Radicale extension views."""

from django.views import generic

from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth.models import Permission


class CalendarDetailView(auth_mixins.LoginRequiredMixin, generic.TemplateView):
    """Calendar detail view."""

    template_name = "modoboa_radicale/calendar_display.html"

    def get_context_data(self, **kwargs):
        """Include extra information."""
        context = super(CalendarDetailView, self).get_context_data(**kwargs)
        permissions = (
            self.request.user.user_permissions.all() |
            Permission.objects.filter(group__user=self.request.user)
        ).select_related("content_type")
        permissions = [
            "{}.{}".format(p.content_type.app_label, p.codename)
            for p in permissions
        ]
        context.update({"selection": "radicale", "permissions": permissions})
        return context
