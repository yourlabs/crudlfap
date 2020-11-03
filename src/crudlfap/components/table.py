from django.core.paginator import Paginator

from ryzom.components import Component
from ryzom.components.muicss import Form


class Table(Component):
    tag = 'table'

    def __init__(self, dataset, per_page=None, columns=None, labels=None, *args, **kwargs):
        self.dataset = dataset
        self.paginator = Paginator(self.dataset, per_page or 30)
        self.columns = columns or [key for key in dataset[0].keys()]
        self.labels = labels or dict()
        for key in self.columns:
            self.labels.setdefault(key, key)
        super().__init__(*args, **kwargs)

    def render(self, context=None):
        if header := self.header():
            self.content.append(header)
        if body := self.body():
            self.content.append(body)

    def header(self):
        return Component(
            Component(
                *[self.th(column) for column in self.columns],
                tag='tr',
            ),
            tag='thead',
        )

    def th(self, key):
        return Component(self.labels[key], tag='th')

    def body(self):
        return Component(
            *[self.row(item) for item in self.dataset],
            tag='tbody',
        )

    def row(self, item):
        return Component(*[
            self.cell(item, column)
            for column in self.columns
        ], tag='tr')

    def cell(self, item, column):
        return Component(item.get(column, ''), tag='td')