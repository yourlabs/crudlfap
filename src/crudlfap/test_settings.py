from importlib import reload
import sys
import warnings

import pytest

pytest_plugins = ["pytester"]


def get_settings():
    if "crudlfap.settings" in sys.modules:
        return reload(sys.modules["crudlfap.settings"])
    else:
        from crudlfap import settings

        return settings


@pytest.mark.parametrize("value, expected", (
    ("1", True),
    ("0", False),
    (None, False),
))
def test_DEBUG_from_int(monkeypatch, value, expected):
    if value is None:
        monkeypatch.delenv("DEBUG", raising=False)
    else:
        monkeypatch.setenv("DEBUG", value)

    assert get_settings().DEBUG is expected


def test_DEBUG_invalid(monkeypatch):
    monkeypatch.setenv("DEBUG", "invalid")

    with warnings.catch_warnings(record=True) as cw:
        get_settings()

    assert len(cw) == 1
    assert str(cw[0].message).startswith(
        "invalid DEBUG environment variable ('invalid'): invalid literal"
    )


@pytest.mark.parametrize("DEBUG", ("0", "1"))
def test_logging_settings(DEBUG, testdir):
    """Check logging setup/settings.

    Runs in pytest subprocess to check settings before/after django.setup(),
    which pytest-django calls with DJANGO_SETTINGS_MODULE being set before
    already.
    """
    testdir.monkeypatch.setenv("DEBUG", DEBUG)
    testdir.monkeypatch.delenv("DJANGO_SETTINGS_MODULE", raising=False)

    p1 = testdir.makepyfile(
        r"""
        import logging
        import os

        import django
        import pytest
        from django.core.exceptions import ImproperlyConfigured


        assert os.environ["DEBUG"] == {DEBUG!r}

        def test_inner(monkeypatch, request, capfd):
            default_level = logging.WARNING

            root_logger = logging.getLogger()
            assert root_logger.level == default_level
            root_handlers = root_logger.handlers[:]

            djangodb_logger = logging.getLogger("django.db")
            assert djangodb_logger.level == logging.NOTSET

            with pytest.raises(ImproperlyConfigured):
                django.setup()

            monkeypatch.setenv("DJANGO_SETTINGS_MODULE", "crudlfap.settings")
            django.setup()

            from django.conf import settings

            if {DEBUG}:
                assert settings.DEBUG is True
                assert djangodb_logger.level == logging.DEBUG
                assert root_logger.level == logging.DEBUG
            else:
                assert settings.DEBUG is False
                assert djangodb_logger.level == logging.NOTSET
                assert root_logger.level == logging.INFO

            # "console" stream handler for root logger gets added.
            assert [
                isinstance(x, logging.StreamHandler)
                for x in root_logger.handlers
                if x not in root_handlers
            ] == [True]

            djangodb_logger.debug("test_debug")
            djangodb_logger.warning("test_warning")

            # Only propagated once to console handler.
            out, err = capfd.readouterr()
            assert out == ""
            if {DEBUG}:
                assert err == "DEBUG test_debug\nWARNING test_warning\n"
            else:
                assert err == "WARNING test_warning\n"
        """.format(
            DEBUG=DEBUG,
        )
    )
    result = testdir.runpytest_subprocess("-p", "no:django", str(p1))
    assert result.ret == 0
