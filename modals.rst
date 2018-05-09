Dynamic resize
==============

Modals should resize automatically based on content width and
height, using MutationObserver with an idempotent callback.

Positionings
============

Small
-----

Centered title and button::

    +-------------------------------+
    |                               |
    |                               |
    |                               |
    |      +----------------+       |
    |      | Title          |       |
    |      |         Button |       |
    |      +----------------+       |
    |                               |
    |                               |
    |                               |
    +-------------------------------+

Medium
------

With content fitting in height and width in the screen::

    +-------------------------------+
    |                               |
    |    +--------------------+     |
    |    | Title              |     |
    |    | Additionnal text   |     |
    |    | Content, form      |     |
    |    | fields ....        |     |
    |    |             Button |     |
    |    +--------------------+     |
    |                               |
    +-------------------------------+

Large
-----

With content that does not fit in height nor in width, scroll inside content::

    +-------------------------------+
    |+-----------------------------+|
    || Title                      ^||
    || Additionnal text           ‖||
    || Content, form              ‖||
    || fields ....                ‖||
    || fields ....                ‖||
    || fields ....                ‖||
    ||<==========================>V||
    ||                      Button ||
    |+-----------------------------+|
    +-------------------------------+

Bonus features
==============

Undo modal close
----------------

Also call M.toast on modal close, with a link to reopen modal.

Title bar
---------

In later version or if possible, also treat title bar like button bar and add
close button::

    +-------------------------------+
    |+-----------------------------+|
    || Title                      X||
    || Additionnal text           ^||
    || Content, form              ‖||
    || fields ....                ‖||
    || fields ....                ‖||
    || fields ....                ‖||
    ||<==========================>V||
    ||                      Button ||
    |+-----------------------------+|
    +-------------------------------+
