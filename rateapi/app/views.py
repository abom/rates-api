from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from rates.providers import FetchError
from .helpers import NoRatesError, fetch_and_save_rate, get_current_rate, is_authenticated


class NoRatesAPIError(APIException):
    status_code = 503
    default_detail = "no exchange rates have been fetched, please force fetch the rates or try again later"
    default_code = "no_rates_found"


class FetchErrorAPIError(APIException):
    status_code = 400
    default_detail = "error while fetching rates"
    default_code = "rate_fetch_error"


class AuthenticationAPIError(APIException):
    status_code = 401
    default_detail = "X-API-Key header is missing or not valid"
    default_code = "authentication_error"


def auth(function):
    def wrap(request, *args, **kwargs):
        try:
            key = request.headers.get("x-api-key", "")
            if not key:
                raise AuthenticationAPIError

            if is_authenticated(key):
                return function(request, *args, **kwargs)
            else:
                raise AuthenticationAPIError
        except AuthenticationAPIError as e:
            return JsonResponse(e.get_full_details(), status=status.HTTP_401_UNAUTHORIZED)

    return wrap


@csrf_exempt
@auth
@api_view(["GET", "POST"])
def rate_view(request):
    if request.method == "GET":
        try:
            rate = get_current_rate()
        except NoRatesError:
            raise NoRatesAPIError

        return Response(rate)

    if request.method == "POST":
        try:
            fetch_and_save_rate()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except FetchError as e:
            raise FetchErrorAPIError(detail=e)

    return Response("unknown method", status=status.HTTP_405_METHOD_NOT_ALLOWED)
