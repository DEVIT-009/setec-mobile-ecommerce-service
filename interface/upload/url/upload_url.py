from django.urls import path
from interface.upload.view.upload_view import CloudinarySignatureView, ConfirmUploadView

urlpatterns = [
    path('cloudinary-signature/', CloudinarySignatureView.as_view(), name='upload-cloudinary-signature'),
    path('confirm/', ConfirmUploadView.as_view(), name='upload-confirm'),
]
