"""Radicale extension forms."""

from django import forms
from django.utils.translation import ugettext_lazy

from modoboa.lib import form_utils
from modoboa.parameters import forms as param_forms


class ParametersForm(param_forms.AdminParametersForm):
    """Global parameters."""

    app = "modoboa_radicale"

    server_settings = form_utils.SeparatorField(
        label=ugettext_lazy("Server settings")
    )

    server_location = forms.CharField(
        label=ugettext_lazy("Server URL"),
        help_text=ugettext_lazy(
            "The URL of your Radicale server. "
            "It will be used to construct calendar URLs."
        ),
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )

    rights_management_sep = form_utils.SeparatorField(
        label=ugettext_lazy("Rights management"))

    rights_file_path = forms.CharField(
        label=ugettext_lazy("Rights file's path"),
        initial="/etc/modoboa_radicale/rights",
        help_text=ugettext_lazy(
            "Path to the file that contains rights definition"
        ),
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    allow_calendars_administration = form_utils.YesNoField(
        label=ugettext_lazy("Allow calendars administration"),
        initial=False,
        help_text=ugettext_lazy(
            "Allow domain administrators to manage user calendars "
            "(read and write)"
        )
    )
