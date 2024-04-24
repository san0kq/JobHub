from __future__ import annotations

from typing import TYPE_CHECKING
from logging import getLogger

from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views import View
from django.conf import settings

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

from accounts.presentation.web.forms import RegistrationForm
from core.presentation.common import convert_data_from_request_to_dto
from core.business_logic.dto import RegistrationDTO
from core.business_logic.exceptions import (
    ConfirmationCodeExpired,
    ConfirmationCodeNotExists,
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
)
from core.business_logic.services import (
    confirm_user_email,
    create_user
)

logger = getLogger(__name__)


class RegistrationView(View):
    """
    View for user registration.

    Methods:
        - get(request: HttpRequest) -> HttpResponse: Method to handle GET requests for displaying the registration form.
        - post(request: HttpRequest) -> HttpResponse: Method to handle POST requests for user registration.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handle GET requests for displaying the registration form.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The HTTP response containing the registration form.
        """
        if request.user.is_authenticated:
            return redirect('core:main')

        form = RegistrationForm()

        context = {
            'form': form,
        }
        
        return render(request, 'registration.html', context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Handle POST requests for user registration.

        Args:
            request (HttpRequest): The HTTP request object containing user registration data.

        Returns:
            HttpResponse: The HTTP response after processing the registration attempt.
        """
        form = RegistrationForm(request.POST)
        context = {"form": form}

        if form.is_valid():
            error_message = None
            success_message = None

            data: RegistrationDTO = convert_data_from_request_to_dto(
                dto=RegistrationDTO, data_from_form=form.cleaned_data
            )


            try:
                is_send_code = create_user(data=data)

                if is_send_code['result']:
                    success_message: str | None = (
                        f'Confirmation email sent. Please confirm it by the link. Check {data.email.lower()}'
                    )
                
                elif not is_send_code['result']:
                    time_to_expire = is_send_code['time_to_expire']
                    minutes = time_to_expire // 60
                    seconds = int(time_to_expire % 60)
                    error_message = f'You can send the code no more frequently than once every {settings.CONFIRMATION_CODE_LIFETIME / 60} minutes. The next attempt is in: {minutes} minute and {seconds} seconds.'
                    context.update({'error_message': error_message})

            except EmailAlreadyExistsError:
                error_message = (
                    f'The email address {data.email.lower()} already exists.'
                )
            except UsernameAlreadyExistsError:
                error_message = f'The username {data.username.lower()} already exists.'

            context.update({
                'success_message': success_message,
                'error_message': error_message
            })

        return render(request, 'registration.html', context=context)


class ConfirmEmailView(View):
    """
    View for confirming user email address.

    Methods:
        - get(request: HttpRequest) -> HttpResponse: Method to handle GET requests for confirming user email.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handle GET requests for confirming user email.

        Args:
            request (HttpRequest): The HTTP request object containing confirmation parameters.

        Returns:
            HttpResponse: The HTTP response after confirming user email.
        """
        confirmation_code = request.GET['code']
        email = request.GET['email']
        try:
            confirm_user_email(
                confirmation_code=confirmation_code, email=email
            )
        except ConfirmationCodeNotExists:
            return HttpResponseBadRequest(content='Invalid confirmation code.')
        except ConfirmationCodeExpired:
            return HttpResponseBadRequest(content='Confirmation code expired.')


        return redirect(to='accounts:login')
