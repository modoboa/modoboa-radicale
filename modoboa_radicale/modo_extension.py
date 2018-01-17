"""Radicale management frontend."""

from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy

from modoboa.core.extensions import ModoExtension, exts_pool
from modoboa.parameters import tools as param_tools

from . import __version__
from . import forms


class Radicale(ModoExtension):
    """Radicale extension declaration."""

    name = "modoboa_radicale"
    label = ugettext_lazy("Radicale management")
    topredirection_url = reverse_lazy("modoboa_radicale:index")
    version = __version__
    url = "calendars"
    description = ugettext_lazy(
        "Management frontend for Radicale, a simple calendar and contact "
        "server."
    )

    def load(self):
        """Plugin loading."""
        param_tools.registry.add(
            "global", forms.ParametersForm, "Radicale")

exts_pool.register_extension(Radicale)
