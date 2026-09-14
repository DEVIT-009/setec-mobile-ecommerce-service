from rest_framework import status
from rest_framework.response import Response


class ResponseHandler:

    @staticmethod
    def success(data, message="Operation successful", paging=None):
        response = {
            "status": "success",
            "message": message,
            "data": data
        }
        if paging:
            response["paging"] = paging
        return Response(response, status=status.HTTP_200_OK)

    @staticmethod
    def created(data, message="Created successfully"):
        return Response({
            "status": "success",
            "message": message,
            "data": data
        }, status=status.HTTP_201_CREATED)

    @staticmethod
    def updated(data, message="Updated successfully"):
        return Response({
            "status": "success",
            "message": message,
            "data": data
        }, status=status.HTTP_200_OK)

    @staticmethod
    def deleted(message=None, data=None):
        return Response({
            "message": message or "Deleted successfully",
            "data": data
        }, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def bad_request(message=None, data=None):
        return Response({
            "message": message or "Bad request",
            "data": data
        }, status=status.HTTP_400_BAD_REQUEST)

    # ------------------------------------------------------------------
    # eCommerce API standard format: {data, meta, errors}
    # ------------------------------------------------------------------

    @staticmethod
    def api_success(data, request_id=None, http_status=status.HTTP_200_OK):
        return Response({
            "data": data,
            "meta": {"request_id": request_id},
            "errors": []
        }, status=http_status)

    @staticmethod
    def api_created(data, request_id=None):
        return Response({
            "data": data,
            "meta": {"request_id": request_id},
            "errors": []
        }, status=status.HTTP_201_CREATED)

    @staticmethod
    def api_no_content():
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def api_list(data, page, page_size, total, request_id=None):
        has_next = (page * page_size) < total
        return Response({
            "data": data,
            "meta": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "has_next": has_next,
                "request_id": request_id,
            },
            "errors": []
        }, status=status.HTTP_200_OK)

    @staticmethod
    def api_error(errors, request_id=None, http_status=status.HTTP_400_BAD_REQUEST):
        return Response({
            "data": None,
            "meta": {"request_id": request_id},
            "errors": errors
        }, status=http_status)
