from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest

from accounts.presentation.web.forms import ProfileEditForm
from core.business_logic.dto import ProfileEditDTO

from core.business_logic.services import (
    get_client_profile,
    get_freelancer_profile,
    initial_profile_form,
    profile_edit
)
from core.presentation.common import convert_data_from_request_to_dto


class ProfileView(LoginRequiredMixin, View):
    """
    Controller for the profile page.

    Supports only GET requests.

    This controller handles only the profile of the authenticated
    user..

    If the user is not authenticated, it redirects to the login page.
    """

    login_url = "accounts:login"

    def get(self, request: HttpRequest) -> HttpResponse:
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
    Controller for editing user profile. Supports both GET and POST requests.
    If the user is not authenticated, it redirects to the login page.
    """

    login_url = "accounts:login"

    def get(self, request: HttpRequest) -> HttpResponse:
        profile_type = request.session.get('profile_type', 'freelancer')

        user = request.user
        initial_data = initial_profile_form(
            user_id=user.pk,
            profile_type=profile_type
        )
        form = ProfileEditForm(initial=initial_data)

        context = {"form": form, 'profile_type': profile_type}
        return render(request, "profile_edit.html", context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
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
                profile_type=profile_type    
            )
      
            return redirect("accounts:profile")

        else:
            context = {"form": form}
            return render(request, "profile_edit.html", context=context)


# class AvatarDeleteView(LoginRequiredMixin, View):
#     login_url = "accounts:login"

#     def get(self, request: HttpRequest) -> HttpResponse:
#         user = request.user
#         delete_profile_avatar(user=user)

#         return redirect("accounts:profile")
