import importlib
from typing import Any, Dict, List, Optional


SOURCEREF = List[Dict[str, Optional[Dict[str, Any]]]]

__all__ = (
    'add_optional_dep',
    'install_optional',
)


if 'ModuleNotFoundError' not in globals():
    ModuleNotFoundError = ImportError


def module_installed(module: str) -> bool:
    """
    Determines if a given module string can be resolved

    Determine if the module referenced by string, can be imported by trying
    an import in two ways:

    - direct import of the module
    - import of the module minus the last part, then see if the last part is
      an attribute of the module.

    Parts of course, are separated by dots.

    :param module: module reference
    :return: True if importable, False otherwise
    """
    have_module = False
    try:
        importlib.__import__(module)
    except ModuleNotFoundError:
        mod_path, dot, cls = module.rpartition('.')
        if not mod_path:
            return False
        try:
            mod = importlib.import_module(mod_path)
        except ModuleNotFoundError:
            return False
        else:
            if hasattr(mod, cls):
                have_module = True
    else:
        have_module = True

    return have_module


def add_optional_dep(module: str, to: List[str], before: str = None,
                     after: str = None):
    """
    Adds an optional dependency

    Add an optional dependency to the given `to` list, if it is resolvable
    by the importer.

    The module can be inserted at the right spot by using before or after
    keyword arguments. If both are given, the gun is pointing at your feet
    and before wins. If neither are given, the module is appended at the
    end.

    :param module: module to add, as it would be added to the given `to` list
    :param to: list to add the module to
    :param before: module string as should be available in the to list.
    :param after: module string as should be available in the to list.
    """
    if not module_installed(module):
        return

    if not before and not after:
        to.append(module)
        return

    try:
        if before:
            pos = to.index(before)
        else:
            pos = to.index(after) + 1
    except ValueError:
        pass
    else:
        to.insert(pos, module)


def install_optional(source: SOURCEREF, target: List[str]):
    """
    Install optional modules

    Add a module as provided by the source reference to the target list. The
    source reference is a list of dictionaries:

    - key: module reference that needs to be inserted
    - value: a dictionary matching the keyword arguments to `add_optional_dep`:
        - before: module reference in `target`; the module will be inserted
                  before this module.
        - after: module reference in `target`; the module will be inserted
                 after this module.
        If value is `None`, the module will be appended to `target`.

    :param source: modules to install
    :param target: install into this list.
    """
    for app in source:
        for ref, kwargs in app.items():
            kwargs = kwargs or {}
            add_optional_dep(ref, target, **kwargs)
