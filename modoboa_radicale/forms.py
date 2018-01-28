"""Radicale extension forms."""

import re

from django import forms
from django.urls import reverse
from django.utils.translation import ugettext as _, ugettext_lazy

from modoboa.admin.models import Domain, Mailbox
from modoboa.lib.email_utils import split_mailbox
from modoboa.lib.exceptions import BadRequest
from modoboa.lib import form_utils
from modoboa.lib.web_utils import render_to_json_response
from modoboa.parameters import forms as param_forms

from .models import UserCalendar, SharedCalendar, AccessRule


class UserCalendarForm(forms.ModelForm):
    """User calendar form."""

    class Meta:
        model = UserCalendar
        fields = ('name', 'mailbox', )
        widgets = {
            'mailbox': forms.widgets.Select(
                attrs={
                    "class": "selectpicker", "data-live-search": "true"
                }
            )
        }

    def __init__(self, user, *args, **kwargs):
        """Custom constructor.

        We need the current user to filter the mailbox list.
        """
        super(UserCalendarForm, self).__init__(*args, **kwargs)
        if user.role == 'SimpleUsers':
            del self.fields['mailbox']
        else:
            self.fields['mailbox'].queryset = \
                Mailbox.objects.get_for_admin(user)


class SharedCalendarForm(forms.ModelForm):
    """Shared calendar form."""

    class Meta:
        model = SharedCalendar
        fields = ("name", "domain", )
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "domain": forms.widgets.Select(
                attrs={"class": "selectpicker", "data-live-search": "true"}
            )
        }

    def __init__(self, user, *args, **kwargs):
        """Custom constructor.

        We need the current user to filter the domain list.
        """
        super(SharedCalendarForm, self).__init__(*args, **kwargs)
        self.fields["domain"].queryset = Domain.objects.get_for_admin(user)


class RightsForm(forms.Form, form_utils.DynamicForm):
    """Rights definition form."""

    username = forms.CharField(
        label="", required=False, widget=forms.widgets.TextInput(
            attrs={"placeholder": ugettext_lazy("Username")}
        )
    )
    read_access = forms.BooleanField(
        initial=False, label=_("Read"), required=False
    )
    write_access = forms.BooleanField(
        initial=False, label=_("Write"), required=False
    )

    def __init__(self, *args, **kwargs):
        from django.http import QueryDict

        if "instance" in kwargs:
            self.calendar = kwargs["instance"]
            del kwargs["instance"]
        else:
            self.calendar = None
        super(RightsForm, self).__init__(*args, **kwargs)

        if self.calendar:
            cpt = 1
            for rule in self.calendar.rules.all():
                self._create_field(
                    forms.EmailField, "username_%d" % cpt,
                    rule.mailbox.full_address
                )
                self._create_field(
                    forms.BooleanField, "read_access_%d" % cpt, rule.read
                )
                self._create_field(
                    forms.BooleanField, "write_access_%d" % cpt, rule.write
                )
                cpt += 1

        if args and isinstance(args[0], QueryDict):
            self._load_from_qdict(args[0], "username", forms.EmailField)
            self._load_from_qdict(args[0], "read_access", forms.BooleanField)
            self._load_from_qdict(args[0], "write_access", forms.BooleanField)

    def save(self):
        """Custom save method."""
        usernames = {}
        for name, value in self.cleaned_data.items():
            if not name.startswith("username") or not value:
                continue
            res = re.match(r"[^_]+_(\d+)$", name)
            pos = int(res.group(1)) if res else None
            usernames[value] = pos
        for rule in self.calendar.rules.select_related().all():
            if rule.mailbox.full_address not in usernames:
                rule.delete()
        for username, pos in usernames.items():
            local_part, domname = split_mailbox(username)
            try:
                mbox = Mailbox.objects.get(
                    address=local_part, domain__name=domname
                )
            except Mailbox.DoesNotExist:
                raise BadRequest(_("Mailbox %s does not exist"))
            if pos:
                raccess = self.cleaned_data.get("read_access_%d" % pos, False)
                waccess = self.cleaned_data.get("write_access_%d" % pos, False)
            else:
                raccess = self.cleaned_data.get("read_access", False)
                waccess = self.cleaned_data.get("write_access", False)
            acr, created = AccessRule.objects.get_or_create(
                mailbox=mbox, calendar=self.calendar
            )
            acr.read = raccess
            acr.write = waccess
            acr.save()


class UserCalendarWizard(form_utils.WizardForm):
    """Calendar creation wizard."""

    def __init__(self, request):
        super(UserCalendarWizard, self).__init__(request)
        self.add_step(
            form_utils.WizardStep(
                "general", UserCalendarForm, _("General"),
                new_args=[request.user]
            )
        )
        self.add_step(
            form_utils.WizardStep(
                "rights", RightsForm, _("Rights"),
                formtpl="modoboa_radicale/rightsform.html"
            )
        )

    def extra_context(self, context):
        context.update({
            "title": _("New calendar"),
            "action": reverse("modoboa_radicale:user_calendar_add"),
            "formid": "newcal_form"
        })

    def done(self):
        calendar = self.first_step.form.save(commit=False)
        if self.request.user.role == 'SimpleUsers':
            calendar.mailbox = self.request.user.mailbox
        calendar.save()
        self.steps[1].form.calendar = calendar
        self.steps[1].form.save()
        return render_to_json_response(_("Calendar created"))


class UserCalendarEditionForm(form_utils.TabForms):
    """User calendar edition form."""

    def __init__(self, request, *args, **kwargs):
        self.forms = []
        self.forms.append({
            "id": "general",
            "title": _("General"),
            "cls": UserCalendarForm,
            "mandatory": True,
            "new_args": [request.user]
        })
        self.forms.append({
            "id": "rights",
            "title": _("Rights"),
            "cls": RightsForm,
            "formtpl": "modoboa_radicale/rightsform.html",
            "mandatory": True
        })
        super(UserCalendarEditionForm, self).__init__(request, *args, **kwargs)

    def extra_context(self, context):
        calendar = self.instances["general"]
        context.update({
            "title": self.instances["general"].name,
            "formid": "ucal_form",
            "action": reverse(
                "modoboa_radicale:user_calendar", args=[calendar.id])
        })

    def save(self):
        """Custom save method."""
        self.forms[0]["instance"].save()
        self.forms[1]["instance"].save()

    def done(self):
        return render_to_json_response(_("Calendar updated"))


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
