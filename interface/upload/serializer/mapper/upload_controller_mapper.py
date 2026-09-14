from typing import Dict, Any
from dataclasses import asdict
from interface.upload.serializer.response.upload_response import (
    CloudinarySignatureResponse,
    UploadResponse,
)


class UploadControllerMapper:

    @staticmethod
    def signature_to_response(data: Dict[str, Any]) -> Dict[str, Any]:
        response_dto = CloudinarySignatureResponse(
            timestamp=data["timestamp"],
            signature=data["signature"],
            api_key=data["api_key"],
            cloud_name=data["cloud_name"],
            folder=data["folder"],
        )
        return asdict(response_dto)

    @staticmethod
    def to_response(data: Dict[str, Any]) -> Dict[str, Any]:
        response_dto = UploadResponse(
            id=str(data.get("id")) if data.get("id") else None,
            user_id=str(data.get("user_id")) if data.get("user_id") else None,
            public_id=data.get("public_id", ""),
            url=data.get("url", ""),
            secure_url=data.get("secure_url"),
            mime_type=data.get("mime_type"),
            usage_type=data.get("usage_type"),
            created_at=data.get("created_at"),
        )
        return asdict(response_dto)
