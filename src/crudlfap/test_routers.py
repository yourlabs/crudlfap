import re

from crudlfap import crudlfap

from django.db import models

import pytest


class Artist(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)

    class Meta:
        managed = False
        app_label = 'crudlfap_test'


class ArtistPicture(models.Model):
    path = models.ImageField(upload_to='lol')

    class Meta:
        managed = False
        app_label = 'crudlfap_test'
        verbose_name = 'Artist photo'


def assert_url_like(view, name, pattern):
    url = view.as_url()
    assert url.name == name
    assert url.regex == re.compile(pattern)


@pytest.fixture
def router():
    return crudlfap.Router(Artist)


def test_router_init():
    result = crudlfap.Router(Artist)
    assert result.model == Artist
    assert result.prefix == ''


def test_router_create(router):
    assert_url_like(
        router['create'],
        'artist_create',
        'create/$'
    )


def test_router_detail(router):
    assert_url_like(
        router['detail'],
        'artist_detail',
        '(?P<slug>[\w\d_-]+)/detail/$'
    )


def test_router_delete(router):
    assert_url_like(
        router['delete'],
        'artist_delete',
        '(?P<slug>[\w\d_-]+)/delete/$'
    )


def test_router_list(router):
    assert_url_like(
        router['list'],
        'artist_list',
        '$'
    )


def test_router_update(router):
    assert_url_like(
        router['update'],
        'artist_update',
        '(?P<slug>[\w\d_-]+)/update/$'
    )


@pytest.fixture
def router_prefix():
    return crudlfap.Router(ArtistPicture, prefix='photo/')


def test_router_prefix(router_prefix):
    assert router_prefix.model == ArtistPicture
    assert router_prefix.prefix == 'photo/'


def test_router_prefix_create(router_prefix):
    assert_url_like(
        router_prefix['create'],
        'artistpicture_create',
        'photo/create/$'
    )


def test_router_prefix_detail(router_prefix):
    assert_url_like(
        router_prefix['detail'],
        'artistpicture_detail',
        'photo/(?P<pk>\d+)/detail/$'
    )


def test_router_prefix_delete(router_prefix):
    assert_url_like(
        router_prefix['delete'],
        'artistpicture_delete',
        'photo/(?P<pk>\d+)/delete/$'
    )


def test_router_prefix_list(router_prefix):
    assert_url_like(
        router_prefix['list'],
        'artistpicture_list',
        'photo/$'
    )


def test_router_prefix_update(router_prefix):
    assert_url_like(
        router_prefix['update'],
        'artistpicture_update',
        'photo/(?P<pk>\d+)/update/$'
    )
