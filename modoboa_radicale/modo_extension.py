"""
Radicale management frontend.

"""

from django.utils.translation import ugettext_lazy

from modoboa.core.extensions import ModoExtension, exts_pool
from modoboa.lib import parameters

from . import __version__


class Radicale(ModoExtension):

    """Radicale extension declaration."""

    name = "modoboa_radicale"
    label = ugettext_lazy("Radicale management")
    version = __version__
    url = "calendars"
    description = ugettext_lazy(
        "Management frontend for Radicale, a simple calendar and contact "
        "server."
    )

    def load(self):
        """Plugin loading."""
        from .app_settings import ParametersForm

        parameters.register(ParametersForm, "Radicale")
        from . import general_callbacks

exts_pool.register_extension(Radicale)
