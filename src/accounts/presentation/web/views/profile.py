from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.forms import formset_factory

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest

from accounts.presentation.web.forms import ProfileEditForm
from core.business_logic.dto import ProfileEditDTO

from core.business_logic.services import (
    get_client_profile,
    get_freelancer_profile,
    initial_profile_form,
    profile_edit,
    delete_profile_avatar
)
from core.presentation.common import convert_data_from_request_to_dto


class ProfileView(LoginRequiredMixin, View):
    """
    View for displaying user profile information.

    Methods:
        - get(request: HttpRequest) -> HttpResponse: Method to handle GET requests for displaying the user profile.
    """

    login_url = 'accounts:login'

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handle GET requests for displaying the user profile.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The HTTP response containing the user profile information.
        """
        profile_type = request.session.get('profile_type')
        user = request.user
        if profile_type == 'client':
            profile = get_client_profile(user_id=user.pk)
            if profile:
                context = {'profile': profile, 'profile_type': profile_type}
                return render(
                    request,
                    'profile.html',
                    context=context
                )
        else:
            profile = get_freelancer_profile(user_id=user.pk)
            if profile:
                context = {'profile': profile, 'profile_type': profile_type}
                return render(
                    request,
                    'profile.html',
                    context=context
                )
            
        if not profile:
            return redirect('accounts:profile_edit')


class ProfileEditView(LoginRequiredMixin, View):
    """
    View for editing user profile information.

    Methods:
        - get(request: HttpRequest) -> HttpResponse: Method to handle GET requests for displaying the profile edit form.
        - post(request: HttpRequest) -> HttpResponse: Method to handle POST requests for updating user profile.
    """

    login_url = 'accounts:login'

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handle GET requests for displaying the profile edit form.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The HTTP response containing the profile edit form.
        """
        profile_type = request.session.get('profile_type', 'freelancer')

        user = request.user
        initial_data = initial_profile_form(
            user_id=user.pk,
            profile_type=profile_type
        )
        form = ProfileEditForm(initial=initial_data)

        context = {
            'form': form,
            'profile_type': profile_type,
            'avatar': initial_data.get('avatar')
        }
        return render(request, 'profile_edit.html', context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Handle POST requests for updating user profile.

        Args:
            request (HttpRequest): The HTTP request object containing profile update data.

        Returns:
            HttpResponse: The HTTP response after processing the profile update.
        """
        profile_type = request.session.get('profile_type', 'freelancer')

        user = request.user
        form = ProfileEditForm(request.POST, files=request.FILES)

        if form.is_valid():
            data = convert_data_from_request_to_dto(
                dto=ProfileEditDTO, data_from_form=form.cleaned_data
            )

            profile_edit(
                data=data,
                user=user,
                profile_type=profile_type,
            )
      
            return redirect('accounts:profile')

        else:
            context = {'form': form}
            return render(request, 'profile_edit.html', context=context)


class AvatarDeleteView(LoginRequiredMixin, View):
    """
    View for deleting user avatar.

    Methods:
        - get(request: HttpRequest, profile_type: str) -> HttpResponse: Method to handle GET requests for deleting user avatar.
    """

    login_url = 'accounts:login'

    def get(self, request: HttpRequest, profile_type: str = 'freelancer') -> HttpResponse:
        """
        Handle GET requests for deleting user avatar.

        Args:
            request (HttpRequest): The HTTP request object.
            profile_type (str): The type of profile (e.g., 'freelancer' or 'client').

        Returns:
            HttpResponse: The HTTP response after deleting the user avatar.
        """
        user = request.user
        delete_profile_avatar(user=user, profile_type=profile_type)

        return redirect('accounts:profile')
