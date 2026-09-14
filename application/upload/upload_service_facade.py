import hashlib
import time
from typing import Dict, Any
from django.conf import settings
from domain.upload.service.upload_service import UploadServiceInterface


class UploadServiceFacade(UploadServiceInterface):

    def generate_signature(self, folder: str = "uploads") -> Dict[str, Any]:
        cloud_name = getattr(settings, 'CLOUDINARY_CLOUD_NAME', '')
        api_key = getattr(settings, 'CLOUDINARY_API_KEY', '')
        api_secret = getattr(settings, 'CLOUDINARY_API_SECRET', '')
        timestamp = int(time.time())
        params = f"folder={folder}&timestamp={timestamp}{api_secret}"
        signature = hashlib.sha1(params.encode()).hexdigest()
        return {
            "api_key": api_key,
            "timestamp": timestamp,
            "signature": signature,
            "cloud_name": cloud_name,
            "folder": folder,
        }

    def confirm_upload(self, user_id: str, data: dict) -> Dict[str, Any]:
        return {
            "public_id": data.get('public_id'),
            "url": data.get('url'),
            "secure_url": data.get('secure_url'),
            "mime_type": data.get('mime_type'),
            "usage_type": data.get('usage_type'),
        }
