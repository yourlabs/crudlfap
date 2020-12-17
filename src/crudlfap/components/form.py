import re
from collections.abc import Iterable
from django.utils.module_loading import import_string

from ryzom.components import Component, Text
from ryzom.components.django import Factory
from django.utils.html import conditional_escape


class TextInput(Component):
    def __init__(self, widget):
        attrs = widget['attrs']
        attrs.update({
            'name': widget['name'],
            'type': widget.get('type', 'text'),
        })
        if widget['value'] is not None:
            attrs['value'] = widget['value']
        return super().__init__(
            tag='mwc-textfield',
            outlined='1',
            label=re.findall('>([^<]*)<', widget['label_tag'])[0],
            **attrs,
        )


class CheckboxInput(Component):
    def __init__(self, widget):
        attrs = widget['attrs']
        return super().__init__(
            Component(tag='mwc-checkbox'),
            tag='mwc-formfield',
            label=re.findall('>([^<]*)<', widget['label_tag'])[0].rstrip(': '),
            **attrs,
        )


class Select(Component):
    def __init__(self, widget):
        options = []
        for group_name, group_choices, group_index in widget['optgroups']:
            for option in group_choices:
                options.append(Component(
                    Text(option['label']),
                    value=option['value'],
                    tag='mwc-list-item',
                ))

        return super().__init__(
            *options,
            tag='mwc-select',
            label=widget['label'],
            outlined=1,
            name=widget['name'],
        )


class NullBooleanSelect(Select):
    pass


class SelectMultiple(Component):
    def __init__(self, widget):
        options = []
        for group_name, group_choices, group_index in widget['optgroups']:
            for option in group_choices:
                options.append(Component(
                    Text(option['label']),
                    value=option['value'],
                    tag='option',
                ))

        super().__init__(
            Component(
                *options,
                multiple='true',
                name=widget['name'],
                tag='select',
                slot='select'
            ),
            Component(
                Component(
                    placeholder='+ ' + widget['label'] + ' ...',
                    slot='input',
                    tag='mwc-textfield',
                ),
                style='display: block',  # like material fields etc
                slot='input',
                tag='autocomplete-light',
            ),
            Component(slot='deck'),
            Component(
                Component(
                    Component(tag='mwc-checkbox', cls='clear', checked=1),
                    tag='mwc-formfield',
                    label='LABEL',
                ),
                tag='template',
                slot='template',
            ),
            multiple='true',
            tag='autocomplete-select'
        )


def Field(field, widget=None, attrs=None, only_initial=False, factory=None):  # noqa: C901 E501
    widget = widget or field.field.widget
    if field.field.localize:
        widget.is_localized = True
    attrs = attrs or {}
    attrs = field.build_widget_attrs(attrs, widget)
    if field.auto_id and 'id' not in widget.attrs:
        attrs.setdefault('id', field.html_initial_id
                         if only_initial else field.auto_id)

    context = widget.get_context(
        name=field.html_initial_name if only_initial else field.html_name,
        value=field.value(),
        attrs=attrs,
    )
    widget_context = context['widget']
    content = []
    html_class_attrs = {'data-component': 'ryzom.components.muicss.Field'}
    errors = field.form.error_class(field.errors)
    css_classes = field.css_classes()  # nice introspection
    if css_classes:
        html_class_attrs = {"class": css_classes}

    # For MuiCheckboxInput
    label_chkbox = ''
    if field.label:
        label = conditional_escape(field.label)
        label_chkbox = label
        label = field.label_tag(label) or ''
    else:
        label = ''

    widget_context['label_tag'] = label
    widget_context['label'] = label_chkbox

    ComponentCls = factory(widget)

    if field.help_text:
        html_class_attrs['helper'] = field.help_text

    if errors:
        html_class_attrs['validationMessage'] = '<br>'.join(errors)
    component = ComponentCls(widget_context,)
    content.extend(
        component if isinstance(component, Iterable) else [component]
    )
    return content
    return Component(*content, **html_class_attrs)


class Form(Component):
    def __init__(self, form, view):
        content = []
        factory = Factory('crudlfap.components.form')

        # form.non_field_errors
        for error in form.non_field_errors():
            content.append(
                Component(Text(error))
            )

        # hidden field errors
        for field in form.hidden_fields():
            if field.errors:
                for error in field.errors:
                    error_text = _('(Hidden field %(name)s) %(error)s') % \
                                 {'name': field.name, 'error': str(error)}
                    content.append(
                        Component(Text(error_text))
                    )

        # form.visible_fields
        for field in form.visible_fields():
            content += Field(field, factory=factory)

        # form.hidden_fields
        for field in form.hidden_fields():
            content += Field(field, factory=form.factory)

        if getattr(view, 'next_url', None):
            content.append(Component(
                type='hidden',
                name='_next',
                value=view.next_url,
            ))
        content.append(Component(
            type='hidden',
            name='csrfmiddlewaretoken',
            value=view.request.META['CSRF_COOKIE'],
            tag='input'
        ))

        invalid = (
            view.request.method == 'POST'
            and form.errors or form.non_field_errors
        )

        super().__init__(
            *content,
            **{
                'id': 'form',
                'action': view.request.get_full_path(),
                'method': 'post',
                'enctype': 'multipart/form-data',
                'data-controller': 'form',
                'data-action': 'submit->form#submit',
                'invalid': invalid,
                'tag': 'form',
            }
        )


class Factory:
    """ Return the class required to render the ~django.forms.Widget. """
    def __init__(self, module):
        self.module = module

    def __call__(self, widget):
        cls = f'{self.module}.{type(widget).__name__}'
        try:
            cls = import_string(cls)
        except ImportError as exc:
            print(f'WARNING Ryzom not found: {cls}.')
            return TextInput
        return cls
