from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.views import APIView
from rest_framework.response import Response

if TYPE_CHECKING:
    from rest_framework.request import Request


class UpdateProfileTypeAPIView(APIView):
    def post(self, request: Request) -> Response:
        profile_type = request.data.get('profile_type')
        request.session['profile_type'] = profile_type
        return Response({'success': True})
