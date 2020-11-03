from ryzom.test import pretty

from crudlfap.components.table import Table

from crudlfap_example.artist.models import Artist
from crudlfap_example.song.models import Song


def test_table():
    table = Table(
        [dict(name='foo', test='y'), dict(name='bar')],
        labels=dict(name='Nombre'),
    )
    result = table.to_html()
    assert pretty(result) == '''
%table
  %thead
    %tr
      %th
        Nombre
      %th
        test
  %tbody
    %tr
      %td
        foo
      %td
        y
    %tr
      %td
        bar
      %td
'''.strip()


def test_columns():
    table = Table(
        [dict(name='foo', test='y')],
        columns=['name'],
    )
    result = table.to_html()
    assert pretty(result) == '''
%table
  %thead
    %tr
      %th
        name
  %tbody
    %tr
      %td
        foo
'''.strip()


def test_pagination():
    table = Table(
        [
            dict(name='foo'),
            dict(name='bar'),
        ],
        columns=['name'],
        per_page=1,
    )
    result = table.render(context=dict())
    assert pretty(result) == '''
%table
  %thead
    %tr
      %th
        name
  %tbody
    %tr
      %td
        bar
'''.strip()
