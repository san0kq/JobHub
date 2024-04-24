from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.views import APIView
from rest_framework.response import Response

if TYPE_CHECKING:
    from rest_framework.request import Request


class UpdateProfileTypeAPIView(APIView):
    """
    API view to update the profile type associated with the current session.

    Methods:
        - post(request: Request) -> Response: Method to handle POST requests for updating profile type.
    """

    def post(self, request: Request) -> Response:
        """
        Handle POST requests to update the profile type.

        Args:
            request (Request): The HTTP request object containing the profile type data.

        Returns:
            Response: JSON response indicating success or failure of the update.
        """
        profile_type = request.data.get('profile_type')
        request.session['profile_type'] = profile_type
        return Response({'success': True})
