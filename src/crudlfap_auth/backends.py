class ViewBackend:
    def authenticate(self, *args):
        """
        Always return ``None`` to prevent authentication within this backend.
        """
        return None

    def has_perm(self, user_obj, perm, obj=None):
        if not obj.authenticate:
            return True

        elif not user_obj.is_authenticated:
            return False

        if user_obj.is_superuser or obj.allowed_groups == 'any':
            return True

        for group in user_obj.groups.all():
            if group.name in obj.allowed_groups:
                return True

        return False
