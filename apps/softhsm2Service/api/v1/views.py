from rest_framework import viewsets
from ...models import genKey_SoftHSM, signature_SoftHSM, verifySignature_SoftHSM
from .serializers import SoftHSmSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.renderers import StaticHTMLRenderer
from .services import gen_key_softhsm2
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

class SoftHsmViewSet(viewsets.ViewSet):
    """
    This viewset automatically provides `genkey`, `signature`, `verify` and
    `delete-key` actions.

    Additionally we also provide an extra `checkBody` action.
    """
    # all swagger's parameters should be defined here
    sw_accessToken_code = openapi.Parameter(
        name='accessToken', type=openapi.TYPE_STRING, default='softhsm2-atnv', description="Token", in_=openapi.IN_QUERY)
    sw_signatureAlgorithm_code = openapi.Parameter(
        name='signatureAlgorithm', type=openapi.TYPE_STRING, default='RS256', description="HS256, HS384, HS512, RS256, \
            RS384, RS512, ES256, ES384, ES512", in_=openapi.IN_QUERY)
    sw_expirationTime_code = openapi.Parameter(
        name='expirationTime', type=openapi.TYPE_INTEGER, default=1462916947752, description="Expiration Time", in_=openapi.IN_QUERY)
    sw_signingInput_code = openapi.Parameter(
        name='signingInput', type=openapi.TYPE_STRING, default="Signing Input", description="Signing Input", in_=openapi.IN_QUERY)
    sw_alias_code = openapi.Parameter(
        name='alias', type=openapi.TYPE_STRING, default="57a6c4fd-f65e-4baa-8a5d-f34812265383", description="Key ID", in_=openapi.IN_QUERY)
    get_response = {
        status.HTTP_500_INTERNAL_SERVER_ERROR: 'INTERNAL_SERVER_ERROR',
        status.HTTP_204_NO_CONTENT: 'NO_CONTENT',
        status.HTTP_200_OK: 'JSON',
    }
    post_response = {
        status.HTTP_500_INTERNAL_SERVER_ERROR: 'INTERNAL_SERVER_ERROR',
        status.HTTP_304_NOT_MODIFIED: 'NOT_MODIFIED',
        status.HTTP_200_OK: 'JSON',
    }
    delete_response = {
        status.HTTP_500_INTERNAL_SERVER_ERROR: 'INTERNAL_SERVER_ERROR',
        status.HTTP_304_NOT_MODIFIED: 'NOT_MODIFIED',
        status.HTTP_200_OK: 'JSON',
    }

    @swagger_auto_schema(method='POST', manual_parameters=[sw_accessToken_code, sw_signatureAlgorithm_code, sw_expirationTime_code], responses=post_response)
    @action(methods=['POST'], detail=False, url_path='gen-key')
    def gen_key_from_softhsm2(self, request):
        accessToken = request.query_params.get('accessToken')
        signatureAlgorithm = request.query_params.get('signatureAlgorithm')
        expirationTime = request.query_params.get('expirationTime')
        kid = gen_key_softhsm2()
        return Response({"result":kid})
    
    @swagger_auto_schema(method='POST', manual_parameters=[sw_accessToken_code, sw_signatureAlgorithm_code, sw_expirationTime_code], responses=post_response)
    @action(methods=['POST'], detail=False, url_path='gen-key')
    def gen_key_from_softhsm2(self, request):
        kid = gen_key_softhsm2()
        return Response({"result":kid})
    
    @swagger_auto_schema(method='POST', manual_parameters=[sw_accessToken_code, sw_signatureAlgorithm_code, sw_expirationTime_code], responses=post_response)
    @action(methods=['POST'], detail=False, url_path='gen-key')
    def gen_key_from_softhsm2(self, request):
        kid = gen_key_softhsm2()
        return Response({"result":kid})
    