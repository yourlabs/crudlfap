from crudlfap.settings import autosettings, basedir


# CRUDLFA+ will add itself and deal with its own optional dependencies, it will
# add django.contrib dependencies too.
INSTALLED_APPS = [
    'crudlfap_example.artist',
    'crudlfap_example.song',
    'crudlfap_example.nondb',
]

# Apparently you're still on your own for intl
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Exemple of how you could add an optional app that will be added to
# INSTALLED_APPS only if importable.
OPTIONAL_APPS = [
    {'dbdiff': {'after': 'crudlfap'}},
]

# Take a leap of faith.
autosettings(
    globals(),
    # Where Django should write its stuff (database, logs, uploads, collected)
    basedir(__file__, '..', '..'),
)
