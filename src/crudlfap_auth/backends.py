class ViewBackend:
    def authenticate(self, *args):
        """
        Always return ``None`` to prevent authentication within this backend.
        """
        return None

    def has_perm(self, user_obj, perm, obj=None):  # noqa
        try:
            if not obj.authenticate:
                return True
        except AttributeError:
            return False

        if not user_obj.is_authenticated:
            return False

        if user_obj.is_superuser:
            return True

        try:
            if obj.allowed_groups == 'any':
                return True
        except AttributeError:
            return False

        for group in user_obj.groups.all():
            if group.name in obj.allowed_groups:
                return True

        return False
