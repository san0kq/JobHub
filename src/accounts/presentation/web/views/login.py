from __future__ import annotations

from typing import TYPE_CHECKING
from logging import getLogger

from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views import View

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

from accounts.presentation.web.forms import LoginForm
from core.business_logic.dto import LoginDTO
from core.business_logic.exceptions import InvalidAuthCredentials
from core.business_logic.services import authenticate_user, get_user_by_email_or_username
from core.presentation.common import convert_data_from_request_to_dto


logger = getLogger(__name__)


class LoginView(View):
    """
    View for handling user login.

    Methods:
        - get(request: HttpRequest) -> HttpResponse: Method to handle GET requests for displaying the login form.
        - post(request: HttpRequest) -> HttpResponse: Method to handle POST requests for user login.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handle GET requests for displaying the login form.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The HTTP response containing the login form.
        """
        if request.user.is_authenticated:
            return redirect('core:main')

        form = LoginForm()
        context = {'form': form}
        return render(request, 'login.html', context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Handle POST requests for user login.

        Args:
            request (HttpRequest): The HTTP request object containing user login data.

        Returns:
            HttpResponse: The HTTP response after processing the login attempt.
        """
        form = LoginForm(request.POST)

        if form.is_valid():
            data = convert_data_from_request_to_dto(
                dto=LoginDTO, data_from_form=form.cleaned_data
            )
            try:
                user = authenticate_user(data=data)
            except InvalidAuthCredentials as err:
                user = get_user_by_email_or_username(email_or_username=data.email_or_username.lower())
                if user and user.check_password(data.password) and not user.is_active:
                    context = {'email': user.email}
                    return render(request, 'not_active_user.html', context=context)
                
                error_message = err
                context = {'form': form, 'error_message': error_message}
                return render(request, 'login.html', context=context)

            login(request=request, user=user)
            return redirect('core:index')

        else:
            context = {'form': form}
            return render(request, 'login.html', context=context)
