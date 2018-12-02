from django.utils.translation import ugettext_lazy as _


class MenuMixin(object):
    def get_title_menu(self):
        """Return title for menu links to this view."""
        return _(self.view_label).capitalize()

    def get_menu(self):
        return None

    def get_menu_kwargs(self):
        return dict()

    def get_menu_views(self):
        views = []
        for view in self.router.views:
            for menu in view.menus:
                if menu in self.menus_display:
                    view = view.clone(
                        request=self.request,
                        **self.menu_kwargs,
                    )

                    if not view().allowed:
                        continue
                    if view.urlname == self.urlname:
                        continue
                    if view.urlname in [v.urlname for v in views]:
                        continue
                    views.append(view)
        return views
