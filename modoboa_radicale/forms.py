"""Radicale extension forms."""

from django import forms
from django.utils.translation import gettext_lazy

from modoboa.lib import form_utils
from modoboa.parameters import forms as param_forms


class ParametersForm(param_forms.AdminParametersForm):
    """Global parameters."""

    app = "modoboa_radicale"

    server_settings = form_utils.SeparatorField(
        label=gettext_lazy("Server settings")
    )

    server_location = forms.URLField(
        label=gettext_lazy("Server URL"),
        help_text=gettext_lazy(
            "The URL of your Radicale server. "
            "It will be used to construct calendar URLs."
        ),
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    rights_management_sep = form_utils.SeparatorField(
        label=gettext_lazy("Rights management"))

    rights_file_path = forms.CharField(
        label=gettext_lazy("Rights file's path"),
        initial="/etc/modoboa_radicale/rights",
        help_text=gettext_lazy(
            "Path to the file that contains rights definition"
        ),
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    allow_calendars_administration = form_utils.YesNoField(
        label=gettext_lazy("Allow calendars administration"),
        initial=False,
        help_text=gettext_lazy(
            "Allow domain administrators to manage user calendars "
            "(read and write)"
        )
    )

    misc_sep = form_utils.SeparatorField(
        label=gettext_lazy("Miscellaneous"))

    max_ics_file_size = forms.CharField(
        label=gettext_lazy("Maximum size of ICS files"),
        initial="10240",
        help_text=gettext_lazy(
            "Maximum size in bytes of imported ICS files "
            "(or KB, MB, GB if specified)")
    )
