from django.contrib.auth.mixins import AccessMixin
from django.urls import reverse, reverse_lazy
from .models import User


class UserOwnershipMixin(AccessMixin):

    login_url = reverse_lazy('main:login')
    permission_denied_message = "You don't have permission to view this page"
    
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk:
            owner_user = User.objects.get(id=pk)
            if request.user != owner_user:
                return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
