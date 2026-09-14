from typing import Dict, Any
from dataclasses import asdict
from interface.auth.serializer.response.auth_response import AuthTokenResponse, AuthMessageResponse


class AuthControllerMapper:

    @staticmethod
    def to_token_response(data: Dict[str, Any]) -> Dict[str, Any]:
        response_dto = AuthTokenResponse(
            access_token=data.get("access_token", ""),
            refresh_token=data.get("refresh_token", ""),
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in"),
            user=data.get("user"),
        )
        return asdict(response_dto)

    @staticmethod
    def to_message_response(message: str) -> Dict[str, Any]:
        response_dto = AuthMessageResponse(message=message)
        return asdict(response_dto)
