from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import ugettext as _
from ryzom_django_mdc.html import *  # noqa


UNPOLY_TARGET_ALL = '#main, .mdc-top-app-bar__title, #drawer .mdc-list'


class A(A):
    attrs = dict(
        up_target=UNPOLY_TARGET_ALL,
        # up_transition='cross-fade',
    )


class Form(Form):
    attrs = dict(
        up_target=A.attrs['up-target'],
        method='post',
    )


class Container(Div):
    sass = '''
    .Container
        display: flex
        flex-direction: column
        align-items: center
        max-width: 960px
        width: 96vw
        margin: auto

    .up-modal .Container
        width: 86vw

    @media screen and (max-width: 500px)
        .up-modal .up-modal-content
            padding: 10px
    '''


class FormContainer(Container):
    sass = '''
    .FormContainer
        max-width: 580px
        .mdc-text-field, .mdc-form-field, .mdc-select, form
            width: 100%
            max-width: 90vw
    '''


class PageMenu(Div):
    attrs = dict(cls='mdc-elevation--z2', style='margin-bottom: 10px')

    def __init__(self, *args, _next=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._next = _next

    def to_html(self, *content, **context):
        if 'page-menu' not in context:
            return super().to_html(*content, **context)

        content = list(content)
        menu = context['page-menu']

        for v in menu:
            if v.urlname == context['view'].urlname:
                continue

            href = v.url
            if self._next:
                if '?' not in href:
                    href += '?'
                href += '&_next=' + self._next
            button = A(
                MDCTextButton(
                    v.label.capitalize(),
                    icon=getattr(v, 'icon', None),
                    tag='span',
                    style={
                        'margin': '10px',
                        'color': getattr(v, 'color', 'inherit'),
                    },
                ),
                href=href,
                style='text-decoration: none',
            )
            if getattr(v, 'controller', None) == 'modal':
                button.attrs.up_modal = '.main-inner'
                del button.attrs['up-target']

            content.append(button)

        return super().to_html(
            *content,
            '<div class="mdc-elevation-overlay"></div>',
            '<div class="mdc-button__ripple"></div>',
            **context,
        )


class Main(Main):
    pass


class ModalClose(Component):
    '''
    Close the modal when inserted by Unpoly.

    This should be the default behaviour of Unpoly, as documented, and is the
    case with modals that do not redirect on the same page, but for modals with
    a form with a ?_next= redirection then surprisingly unpoly does update the
    body but does not close the modal by default.

    This tag registers a compiler that calls up.modal.close() when it
    sees itself, given that unpoly does not execute scripts in
    response that it loads. As such, this tag MUST be in the initial body, but
    outside the elements that you will load in modal.

    Remove this hack when we figure the problem in unpoly.

    Equivalent of::

        Script(
            'up.compiler(".closemodal", function() { up.modal.close(); })',
            cls='closemodal',
        ),
    '''
    attrs = dict(cls='closemodal')

    def py2js():
        up.compiler('.closemodal', lambda: up.modal.close())


class Message(Div):
    icons = dict(
        debug='check_circle',
        info='check_circle',
        success='check_circle',
        warning='warning',
        error='error',
    )
    colors = dict(
        debug='green',
        info='yellow',
        success='green',
        warning='orange',
        error='red',
    )
    style='''
        padding-left: 16px;
        display: flex;
        flex-direction: row;
        align-items: center
    '''
    cls='mdc-card'

    def __init__(self, message, *content, **attrs):
        print(message.level_tag)
        return super().__init__(
            *content,
            MDCIcon(
                self.icons.get(message.level_tag, 'success'),
                style=dict(color=self.colors[message.level_tag]),
            ),
            Div(message, style='margin-left: 16px'),
            **attrs
        )


class Messages(Div):
    def to_html(self, *content, **context):
        msgs = messages.get_messages(context['view'].request)
        if not msgs:
            return ''

        return Div(*[
            Message(message)
            for message in msgs
        ]).to_html(*content, **context)


class Body(Body):
    style = 'margin: 0'

    def __init__(self, *content, **attrs):
        self.drawer = mdcDrawer(id='drawer')
        self.bar = mdcTopAppBar()
        self.main_inner = Div(
            Messages(),
            *content,
            cls='main-inner',
        )
        self.main = Main(
            self.main_inner,
            ModalClose(),
            cls='main mdc-drawer-app-content',
            id='main',
        )
        self.debug = settings.DEBUG
        super().__init__(
            Spinner(),
            self.bar,
            Div(
                self.drawer,
                self.main,
                cls='mdc-top-app-bar--fixed-adjust',
            ),
        )

    def py2js(self):
        up.compiler(
            '[data-mdc-auto-init]',
            lambda el: mdc.autoInit(el.parentElement)
        )
        if self.debug:
            up.log.enable()


class Spinner(Div):
    sass = '''
    .Spinner
        position: fixed
        float: right
        z-index: 20000
        cursor: pointer

        right: 0
        top: 0
        @media only screen and (max-width: 600px)
          right: -24px
          top: -32px

        .lds-dual-ring
          display: inline-block
          width: 80px
          height: 80px

        .lds-dual-ring:after
          content: " "
          display: block
          width: 28px
          height: 28px
          margin: 8px
          border-radius: 50%
          border: 6px solid #fff
          border-color: #1c68de white #1c68de white
          animation: lds-dual-ring 1.2s linear infinite

        @keyframes lds-dual-ring
          0%
            transform: rotate(0deg)

          100%
            transform: rotate(360deg)
    '''  # noqa

    def py2js(self):
        up.proxy.config.slowDelay = 25
        up.compiler('.Spinner', lambda element: [
            up.on('up:proxy:slow', lambda: up.element.show(element)),
            up.on('up:proxy:recover', lambda: up.element.hide(element)),
        ])

    def __init__(self):
        super().__init__(Div(cls='lds-dual-ring'), style='display:none')


def poll():
    def poll_setup(element):
        interval = parseInt(element.getAttribute('poll') or 5000)
        def poll():
            if not document.hidden:
                up.reload(element)
        poll = setInterval(poll, interval)
        def clear():
            clearInterval(poll)
        return clear
    up.compiler('[poll]', poll_setup)

def poll():
    def poll_setup(element):
        interval = parseInt(element.getAttribute('poll') or 5000)

        def poll():
            if not document.hidden:
                up.reload(element)
            setTimeout(poll, interval)
        setTimeout(poll, interval)
    up.compiler('[poll]', poll_setup)

class App(Html):
    body_class = Body
    scripts = [
        'https://unpkg.com/unpoly@1.0.0/dist/unpoly.js',
        poll,
        # 'https://unpkg.com/unpoly@2.0.0-rc9/unpoly.min.js',
        # 'https://unpkg.com/unpoly@2.0.0-rc9/unpoly-migrate.js',
    ]
    stylesheets = [
        'https://unpkg.com/unpoly@1.0.0/dist/unpoly.css',
        # 'https://unpkg.com/unpoly@2.0.0-rc9/unpoly.min.css',
    ]
    sass = '''
    .up-modal .up-modal-viewport
        padding-left: 0
        padding-right: 0
        padding-top: 10px
    '''

    def to_html(self, *content, **context):
        if title := getattr(context['view'], 'title', None):
            self.head.content.append(Title(title))
        return super().to_html(*content, **context)


class NarrowCard(Div):
    style = {
        'max-width': '95vw',
        'margin': 'auto',
        'padding': '1em',
        'margin-top': '2em',
        'button': {
            'width': '100%',
        },
        '.MDCField label': {
            'width': '100%',
        }
    }


@template('crudlfap/form.html', App)
@template('crudlfap/update.html', App)
@template('crudlfap/create.html', App)
class FormTemplate(FormContainer):
    def to_html(self, view, form, **context):
        back = ''
        if next_ := view.request.GET.get('next', ''):
            back = A(
                MDCButton(
                    _('Back'),
                    tag='span',
                ),
                href=next_,
            )
        return super().to_html(
            H3(view.title),
            Form(
                form,
                CSRFInput(view.request),
                back,
                MDCButtonRaised(getattr(view, 'title_submit', _('Submit'))),
            ),
        )


@template('crudlfap/api.html', Html)
class Swagger(Div):
    def py2js(self):
        el = document.getElementById('swagger-ui')
        ui = SwaggerUIBundle({
            url: el.attributes['schema-url'].value,
            dom_id: '#swagger-ui',
            deepLinking: true,
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIStandalonePreset,
            ],
            plugins: [
                SwaggerUIBundle.plugins.DownloadUrl
            ],
            layout: "StandaloneLayout"
        })
        window.ui = ui

    def to_html(self, **context):
        registry = context['view'].registry
        return super().to_html(
            Script(src='/static/swagger-ui-bundle.js'),
            Script(src='/static/swagger-ui-standalone-preset.js'),
            Stylesheet(href='/static/swagger-ui.css'),
            Div(
                id='swagger-ui',
                schema_url=registry.views['schema'].url,
            ),
            **context
        )


@template('crudlfap/home.html', App, Container)
class Home(Div):
    def to_html(self, **context):
        site = Site.objects.get_current()
        return super().to_html(
            H1('Welcome to ' + site.name),
            MDCButtonRaised(
                'Login to continue',
                href=reverse('login'),
                up_target=UNPOLY_TARGET_ALL,
                tag='a',
            ),
            Div('Then, navigate with the menu button at the north west'),
            **context
        )


@template('registration/logged_out.html', App, NarrowCard)
class LoggedOut(Div):
    def to_html(self, **context):
        return super().to_html(
            H1(_('Log out')),
            P(_('Thanks for spending some quality time with the Web site today.')),  # noqa
            A(
                _('Log in again'),
                href=reverse('login'),
            ),
            **context,
        )


@template('crudlfap/detail.html', App)
class ObjectDetail(Div):
    def to_html(self, *content, **context):
        table = MDCDataTable()
        table.thead.attrs.style.display = 'none'
        table.table.attrs.style.width = '100%'
        table.attrs.data_mdc_auto_init = False

        for field in context['view'].display_fields:
            table.tbody.addchild(MDCDataTableTr(
                MDCDataTableTh(field['field'].verbose_name.capitalize()),
                MDCDataTableTd(field['value']),
            ))

        return super().to_html(
            PageMenu(),
            *content,
            NarrowCard(table),
            **context
        )

    def context(self, *content, **context):
        context['page-menu'] = context['view'].router.get_menu(
            'object',
            context['view'].request,
            object=context['view'].object,
        )
        return super().context(*content, **context)


class ListAction(Div):
    style = {'display': 'inline-block'}

    def onclick(element):
        link = element.attributes.href.value + '?'
        for checkbox in document.querySelectorAll('[data-pk]:checked'):
            link += '&pk=' + checkbox.attributes['data-pk'].value
        up.modal.visit(link, {target: '.main-inner'})


class ListActions(Component):
    tag = 'list-actions'
    style = {'display': 'none'}

    class HTMLElement:
        def connectedCallback(self):
            this.previousElementSibling.addEventListener(
                'change',
                this.change.bind(this),
            )

            this.change({
                'target': this.previousElementSibling.querySelector(':checked')
            })

        def change(self, event):
            if event.target and event.target.checked:
                this.style.display = 'block'
            elif not this.previousElementSibling.querySelector(':checked'):
                this.style.display = 'none'


@template('crudlfap/list.html', App)
class ObjectList(Div):
    def context(self, *content, **context):
        context['page-menu'] = context['view'].router.get_menu(
            'model',
            context['view'].request,
        )
        return super().context(*content, **context)

    def to_html(self, *content, **context):
        checkbox = None
        context['listactions'] = context['view'].router.get_menu(
            'list_action',
            context['view'].request,
        )

        if context['listactions']:
            table_checkbox = MDCCheckboxInput()
            table_checkbox.attrs.addcls = 'mdc-data-table__header-row-checkbox'

            checkbox = MDCDataTableTh(
                table_checkbox,
                addcls='mdc-data-table__header-cell--checkbox',
            )
        thead = MDCDataTableThead(tr=MDCDataTableHeaderTr(checkbox))

        for column in context['view'].table.columns:
            thead.tr.addchild(self.th_component(column, **context))

        # align "actions" title to the right with the buttons
        thead.tr.content[-1].attrs.style['text-align'] = 'right'

        table = MDCDataTableResponsive(thead=thead, style={
            'min-width': '100%',
            'border-width': 0,
        })

        for row in context['view'].table.paginated_rows:
            table.tbody.addchild(
                self.row_component(row, **context)
            )

        if context['listactions']:
            table.addchild(self.listactions_component(**context))

        table.addchild(self.pagination_component(**context))

        return super().to_html(
            *content,
            self.drawer_component(**context) or '',
            PageMenu(_next=context['view'].request.path),
            Div(
                self.search_component(**context) or '',
                table,
                cls='mdc-drawer__content',
                style='overflow-y: unset',
            ),
            **context,
        )

    def listactions_component(self, **context):
        return ListActions(
            *[
                ListAction(
                    MDCButton(
                        view.label,
                        icon=view.icon,
                        style='color: ' + getattr(view, 'color', 'inherit'),
                    ),
                    title=view.title,
                    href=view.url,
                    up_modal='.main-inner',
                    up_target=False,
                ) for view in context['view'].listactions
            ],
        )

    def search_component(self, **context):
        search_form = self.search_form_component(**context)

        filterset = getattr(context['view'], 'filterset', None)
        if not filterset:
            return search_form

        toggle = MDCDrawerToggle(
            Button(
                'filter_list',
                cls='material-icons mdc-icon-button',
                style='--mdc-ripple-fg-size:28px; --mdc-ripple-top:10px;',
            ),
            data_drawer_id='page-drawer',
        )

        filters_chips = Div(
            toggle=toggle if context['view'].filterset.form.fields else '',
            search=search_form or '',
            chips=Div(
                cls='mdc-chip-set',
                role='grid',
                style='display: inline-block',
            )
        )

        def remove_filter_url(name):
            get = context['view'].request.GET.copy()
            if name in get:
                del get[name]
            return context['view'].request.path_info + '?' + get.urlencode()

        for bf in filterset.form.visible_fields():
            value = context['view'].request.GET.get(bf.name, '')
            if not value:
                continue
            chip = MDCChip(
                Span(
                    role='button',
                    tabindex='0',
                    cls='mdc-chip__primary-action',
                    text=Span(
                        bf.label,
                        ': ',
                        str(bf.form.cleaned_data[bf.name]),
                        cls='mdc-chip__text',
                    ),
                ),
                icon=I(
                    'cancel',
                    cls=(
                        'material-icons',
                        'mdc-chip__icon',
                        'mdc-chip__icon--trailing',
                    ),
                    tabindex='-1',
                    role='button',
                ),
                tag='a',
                href=remove_filter_url(bf.name),
                up_target='main',
            )
            filters_chips.chips.addchild(chip)
        return filters_chips

    def drawer_component(self, **context):
        filterset = context['view'].filterset
        if not filterset.form.fields:
            return
        form = Form(
            method='get',
            action=context['view'].request.path_info,
            up_autosubmit=True,
            up_delay='200ms',
            up_target='.mdc-drawer__content',
        )
        for key in ('sort', 'q'):
            if key in context['view'].request.GET:
                form.addchild(Input(
                    name=key,
                    value=context['view'].request.GET[key],
                    type='hidden'
                ))
        for bf in filterset.form.visible_fields():
            filterfield = MDCFilterField(
                label=bf.label,
                widget=bf.to_component()
            )
            value = context['view'].request.GET.get(bf.name, '')
            if not value:
                filterfield.widget.style.display = 'none'
            form.addchild(filterfield)
        drawer = Aside(
            MDCDrawerToggle(
                MDCButton(_('Close'), icon='close'),
                data_drawer_id='page-drawer',
                style='text-align: right',
            ),
            Div(
                form,
                cls='mdc-drawer-app-content',
            ),
            id='page-drawer',
            cls='mdc-drawer mdc-drawer--dismissible',
            style='padding: 1em',
        )
        return drawer

    def search_form_component(self, **context):
        search_form = getattr(context['view'], 'search_form', None)

        if not search_form:
            return

        search_form = InlineForm(
            search_form,
            method='get',
            action=context['view'].request.path_info,
            up_autosubmit=True,
            up_delay='200ms',
            up_target='.mdc-data-table, .mdc-chip-set',
            style='margin-left: 14px',
        )
        for k, v in context['view'].request.GET.items():
            if k == 'q':
                continue
            search_form.addchild(Input(
                name=k,
                value=v,
                type='hidden',
            ))
        return search_form

    def row_component(self, row, **context):
        show_checkbox = False
        for listaction in context['listactions']:
            if listaction.clone(object=row.record)().has_perm():
                show_checkbox = True

        if show_checkbox:
            checkboxinput = MDCCheckboxInput(
                data_pk=str(row.record.pk)
            )
            checkboxinput.attrs.addcls = 'mdc-data-table__row-checkbox'
            tr = MDCDataTableTr(
                MDCDataTableTd(
                    checkboxinput,
                    addcls='mdc-data-table__cell--checkbox',
                )
            )
        elif context['listactions']:
            tr = MDCDataTableTr(MDCDataTableTd())
        else:
            tr = MDCDataTableTr()

        for column, cell in row.items():
            # todo: localize values
            tr.addchild(
                MDCDataTableTd(cell, data_label=column.header),
            )
            # todo: if is numeric
            # td.attrs.addcls = 'mdc-data-table__header-cell--numeric'
        return tr

    def th_component(self, column, **context):
        th = MDCDataTableTh(
            wrapper=Div(
                cls='mdc-data-table__header-cell-wrapper',
                label=Div(
                    cls='mdc-data-table__header-cell-label',
                    style='font-weight: 500',
                    text=Text(column.header),
                ),
            )
        )

        # sorting
        if column.orderable:
            th.attrs.addcls = 'mdc-data-table__header-cell--with-sort'
            if column.is_ordered:
                th.attrs.addcls = 'mdc-data-table__header-cell--sorted'
            get = context['view'].request.GET.copy()
            get['sort'] = column.order_by_alias.next
            href = ''.join([
                context['view'].request.path_info,
                '?',
                get.urlencode(),
            ])
            th.wrapper.content += [
                A(
                    cls=(
                        'mdc-icon-button',
                        'material-icons',
                        'mdc-data-table__sort-icon-button',
                    ),
                    aria_label='Sort by dessert',
                    aria_describedby='dessert-status-label',
                    up_target='table',
                    href=href,
                    text=Text(
                        'arrow_upward'
                        if column.order_by_alias.is_descending
                        else 'arrow_downward'
                    ),
                ),
                Div(
                    cls='mdc-data-table__sort-status-label',
                    aria_hidden='true',
                    id='dessert-status-label',
                ),
            ]
        return th

    def pagination_component(self, **context):
        def pageurl(n):
            get = context['view'].request.GET.copy()
            get['page'] = n
            return context['view'].request.path_info + '?' + get.urlencode()

        page = context['view'].table.page
        navigation = Div(
            Div(
                cls='mdc-data-table__pagination-total',
                text=Text(''.join([
                    str(page.start_index()),
                    '-',
                    str(page.paginator.per_page * page.number),
                    ' / ',
                    str(page.paginator.count),
                ]))
            ),
            A(
                cls=(
                    'mdc-icon-button',
                    'material-icons',
                    'mdc-data-table__pagination-button',
                ),
                disabled=page.number == 1,
                href=pageurl(1),
                icon=Div(cls='mdc-button__icon', text=Text('first_page')),
                up_target='.mdc-data-table',
            ),
            A(
                cls=(
                    'mdc-icon-button',
                    'material-icons',
                    'mdc-data-table__pagination-button',
                ),
                disabled=not page.has_previous(),
                icon=Div(cls='mdc-button__icon', text=Text('chevron_left')),
                href=pageurl(
                    page.number - 1
                    if page.has_previous()
                    else 1
                ),
                up_target='.mdc-data-table',
            ),
            A(
                cls=(
                    'mdc-icon-button',
                    'material-icons',
                    'mdc-data-table__pagination-button',
                ),
                disabled=not page.has_next(),
                icon=Div(cls='mdc-button__icon', text=Text('chevron_right')),
                href=pageurl(
                    page.number + 1
                    if page.has_next()
                    else page.paginator.num_pages
                ),
                up_target='.mdc-data-table',
            ),
            A(
                cls=(
                    'mdc-icon-button',
                    'material-icons',
                    'mdc-data-table__pagination-button',
                ),
                disabled=page.paginator.num_pages == page.number,
                icon=Div(cls='mdc-button__icon', text=Text('last_page')),
                href=pageurl(page.paginator.num_pages),
                up_target='.mdc-data-table',
            ),
            cls='mdc-data-table__pagination-navigation',
        )
        perpage = Div(
            Div(
                _('Rows per page'),
                cls='mdc-data-table__pagination-rows-per-page-label'
            ),
            select=MDCSelectPerPage(
                addcls=(
                    'mdc-select--outlined',
                    'mdc-select--no-label',
                    'mdc-data-table__pagination-rows-per-page-select',
                ),
                select=Select(*[
                    Option(
                        str(i),
                        value=i,
                        selected=page.paginator.per_page == i
                    )
                    for i in (3, 5, 7, 10, 25, 100)
                ])
            ),
            cls='mdc-data-table__pagination-rows-per-page',
        )
        return MDCDataTablePagination(
            perpage=perpage,
            navigation=navigation,
        )


class mdcTopAppBar(Header):
    def __init__(self, title='', buttons=None):
        self.title = title
        self.buttons = buttons or []
        super().__init__(
            Div(cls='mdc-top-app-bar__row'),
            cls='mdc-top-app-bar app-bar',
            id='app-bar',
            data_mdc_auto_init='MDCTopAppBar',
        )

    def to_html(self, view, **context):
        self.content[0].content = [Component(
            Section(
                Button(
                    'menu',
                    cls='material-icons mdc-top-app-bar__navigation-icon mdc-icon-button',  # noqa
                ),
                Span(
                    getattr(view, 'title', getattr(settings, 'SITE_NAME', '')),
                    cls='mdc-top-app-bar__title',
                ),
                cls='mdc-top-app-bar__section mdc-top-app-bar__section--align-start',  # noqa
            ),
            cls='mdc-top-app-bar__section mdc-top-app-bar__section--align-start',  # noqa
            tag='section',
        )]
        return super().to_html(**context)

    def nav():
        window.drawer.open = not window.drawer.open

    def close():
        if window.visualViewport.width < 800:
            window.drawer.open = False

    def py2js(self):
        up.compiler('#drawer, #app-bar, #main', self.setup)

    def setup():
        drawer = document.getElementById('drawer')
        app_bar = document.getElementById('app-bar')
        main = document.getElementById('main')

        window.drawer = mdc.drawer.MDCDrawer.attachTo(drawer)
        topAppBar = mdc.topAppBar.MDCTopAppBar.attachTo(app_bar)
        topAppBar.setScrollTarget(main)
        topAppBar.listen('MDCTopAppBar:nav', self.nav)

        for link in drawer.querySelectorAll('a'):
            link.addEventListener('click', self.close)


class mdcDrawer(Aside):
    menu_hooks = []

    def __init__(self, *content, **attrs):
        super().__init__(
            Div(
                *content,
                cls='mdc-drawer__content',
            ),
            cls='mdc-drawer mdc-drawer--dismissible mdc-top-app-bar--fixed-adjust',  # noqa
            data_mdc_auto_init='MDCDrawer',
            **attrs,
        )

    def to_html(self, *content, view, **context):
        request = view.request
        from .site import site

        menu_content = []
        if request.user.is_authenticated:
            menu_content.append(MDCListItem(str(request.user.email)))
        for view in site.get_menu('main', request):
            icon = getattr(view, 'icon', None)
            title = getattr(view, 'title', '')
            attrs = dict()
            if getattr(view, 'unpoly', True):
                attrs['up_target'] = UNPOLY_TARGET_ALL

            menu_content.append(
                MDCListItem(
                    title.capitalize(), icon=icon,
                    href=view.url,
                    style='text-decoration: none',
                    tag='a',
                    **attrs,
                ),
            )
        for hook in self.menu_hooks:
            menu_content = hook(request, menu_content)

        content = menu_content

        if request.session.get('become_user', None):
            content.append(
                A(
                    ' '.join([
                        str(_('Back to your account')),
                        request.session['become_user_realname'],
                    ]),
                    href=reverse('crudlfap:su'),
                    up_target=UNPOLY_TARGET_ALL,
                )
            )

        return super().to_html(MDCList(*content))


class mdcAppContent(Div):
    def __init__(self, *content):
        super().__init__(
            Component(
                *content,
                tag='main',
                cls='main-content',
                id='main-content',
            ),
            cls='mdc-drawer-app-content mdc-top-app-bar--fixed-adjust',
        )


class mdcSwitch(Component):
    def __init__(
        self, name, label=None, value=None, type=None, errors=None, help=None,
        required=False,
    ):
        super().__init__(
            Div(
                Div(cls='mdc-switch__track'),
                Div(
                    Div(cls='mdc-switch__thumb'),
                    Input(
                        type='checkbox',
                        id='id_' + name,
                        role='switch',
                        aria_checked='true' if bool(value) else '',
                        cls='mdc-switch__native-control',
                        checked=bool(value)
                    ),
                    cls='mdc-switch__thumb-underlay',
                ),
                cls='mdc-switch mdc-switch--checked',
                data_mdc_auto_init='MDCSwitch',
            ),
            Label(
                label or name.capitalize(),
                **{'for': 'id_' + name},
            )
        )
