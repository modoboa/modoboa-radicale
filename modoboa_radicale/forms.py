"""Radicale extension forms."""

from django import forms
from django.utils.translation import ugettext_lazy

from modoboa.lib import form_utils
from modoboa.parameters import forms as param_forms

from . import constants

SSL_VERIFY_CHOICES = (
    (constants.VERIFY, ugettext_lazy("Verify")),
    (constants.NO_VERIFY, ugettext_lazy("Skip verification")),
    (constants.PATH, ugettext_lazy("Provide CA bundle"))
)


class ParametersForm(param_forms.AdminParametersForm):
    """Global parameters."""

    app = "modoboa_radicale"

    server_settings = form_utils.SeparatorField(
        label=ugettext_lazy("Server settings")
    )

    server_location = forms.URLField(
        label=ugettext_lazy("Server URL"),
        help_text=ugettext_lazy(
            "The URL of your Radicale server. "
            "It will be used to construct calendar URLs."
        ),
        widget=forms.TextInput(attrs={"class": "form-control"})
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

    misc_sep = form_utils.SeparatorField(
        label=ugettext_lazy("Miscellaneous"))

    max_ics_file_size = forms.CharField(
        label=ugettext_lazy("Maximum size of ICS files"),
        initial="10240",
        help_text=ugettext_lazy(
            "Maximum size in bytes of imported ICS files "
            "(or KB, MB, GB if specified)")
    )

    ssl_verify_cert = forms.ChoiceField(
        choices=SSL_VERIFY_CHOICES,
        initial=constants.VERIFY,
        label=ugettext_lazy("Type of ssl verification"),
        help_text=ugettext_lazy("It might be needed to set to custom "
            "and set a CA bundle or set to 'Skip verification' "
            "in case of a self-signed cert")
        )

    ssl_ca_bundle_path = forms.CharField(
        label=ugettext_lazy("Path to CA bundle"),
        initial="",
        help_text=ugettext_lazy(
            "Path to the CA bundle. ")
        )

    visibility_rules = {
        "ssl_ca_bundle_path": "ssl_verify_cert=path"
        }
