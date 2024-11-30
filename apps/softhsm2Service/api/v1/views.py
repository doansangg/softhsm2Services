from rest_framework import viewsets
from ...models import genKey_SoftHSM, signature_SoftHSM, verifySignature_SoftHSM
from .serializers import SoftHSmSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.renderers import StaticHTMLRenderer
from .services import gen_key_softhsm2, signature_softhsm2, verify_signature_softhsm2
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
    sw_sharedSecret_code = openapi.Parameter(
        name='sharedSecret', type=openapi.TYPE_STRING, default="secret", description="Shared Secret", in_=openapi.IN_QUERY)
    sw_alg_code = openapi.Parameter(
        name='alg', type=openapi.TYPE_STRING, default="ES256", description="alg", in_=openapi.IN_QUERY)
    sw_kid_code = openapi.Parameter(
        name='kid', type=openapi.TYPE_STRING, default="f6ade591-4230-4114-8147-316dde969395", description="kid", in_=openapi.IN_QUERY)
    sw_use_code = openapi.Parameter(
        name='use', type=openapi.TYPE_STRING, default="sig", description="use", in_=openapi.IN_QUERY)
    sw_kty_code = openapi.Parameter(
        name='kty', type=openapi.TYPE_STRING, default="EC", description="kty", in_=openapi.IN_QUERY)
    sw_n_code = openapi.Parameter(
        name='n', type=openapi.TYPE_STRING, default="AJpGcIVu7fmQJLHXeAClhXaJD7SvuABjYiPcT9IbKFWGWj51GgD-CxtyrQGXT0ctGEEsXOzMZM40q-V7GR-5qkJ_OalVTTc_EeKAHao45bZPsPHLxvusNfrfpyhc6JjF2TQhoOqxbgMgQ9L6W9q9fSjgzx-tPlD0d3X0GZOEQ_NYGstZWRRBwHgsxA2IRYtwSH-v76yPpxF9poLIWdnBKtKfSr6UY7p1BrLmMm0DdMhjQLn6j4S_eB-p2WyBwObvsLqO6FdClpZFtGr82Km2uinpHvZ6KJ_MUEW1sijPPI3rIGbaUbLtQJwX5GVynAP5qU2qRVkcsrKt-GeNoz6QNLM", description="n", in_=openapi.IN_QUERY)
    sw_e_code = openapi.Parameter(
        name='e', type=openapi.TYPE_STRING, default="AQAB", description="e", in_=openapi.IN_QUERY)
    sw_crv_code = openapi.Parameter(
        name='crv', type=openapi.TYPE_STRING, default="P-256", description="crv", in_=openapi.IN_QUERY)
    sw_x_code = openapi.Parameter(
        name='x', type=openapi.TYPE_STRING, default="QDpwgxzGm0XdD-3Rgk62wiUnayJDS5iV7nLBwNEX4SI", description="x", in_=openapi.IN_QUERY)
    sw_y_code = openapi.Parameter(
        name='y', type=openapi.TYPE_STRING, default="AJ3IvktOcoICgdFPAvBM44glxcqoHzqyEmj60eATGf5e", description="y", in_=openapi.IN_QUERY)
    sw_signatures_code = openapi.Parameter(
        name='signatures', type=openapi.TYPE_STRING, default="secret", description="signatures", in_=openapi.IN_QUERY)

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
        try:
            accessToken = request.query_params.get('accessToken')
            signatureAlgorithm = request.query_params.get('signatureAlgorithm')
            expirationTime = request.query_params.get('expirationTime')
            kid = gen_key_softhsm2()
            if kid is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print("ERROR:", e)
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={kid}, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(method='POST', manual_parameters=[sw_accessToken_code, sw_signatureAlgorithm_code, sw_signingInput_code, sw_alias_code, sw_sharedSecret_code], responses=post_response)
    @action(methods=['POST'], detail=False, url_path='signature')
    def signature_from_softhsm2(self, request):
        try:
            accessToken = request.query_params.get('accessToken')
            signatureAlgorithm = request.query_params.get('signatureAlgorithm')
            signingInput = request.query_params.get('signingInput')
            alias = request.query_params.get('alias')
            sharedSecret = request.query_params.get('sharedSecret')
            kid = signature_softhsm2()
            if kid is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print("ERROR:", e)
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={kid}, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(method='POST', manual_parameters=[sw_accessToken_code, sw_signatureAlgorithm_code, sw_signingInput_code, sw_alias_code, sw_sharedSecret_code,\
                                                           sw_alg_code, sw_kid_code, sw_use_code, sw_kty_code, sw_n_code, sw_e_code, sw_crv_code, sw_x_code, sw_y_code, sw_signatures_code], responses=post_response)
    @action(methods=['POST'], detail=False, url_path='verify-signature')
    def verify_signature_from_softhsm2(self, request):
        try:
            accessToken = request.query_params.get('accessToken')
            signatureAlgorithm = request.query_params.get('signatureAlgorithm')
            signingInput = request.query_params.get('signingInput')
            alias = request.query_params.get('alias')
            sharedSecret = request.query_params.get('sharedSecret')
            jwksRequestParam =  { 
            "keyRequestParams": {
                "alg": request.query_params.get('alg'),
                "kid": request.query_params.get('kid'),
                "use": request.query_params.get('use'),
                "kty": request.query_params.get('kty'),
                "n": request.query_params.get('n'),
                "e": request.query_params.get('e'),
                "crv": request.query_params.get('crv'),
                "x": request.query_params.get('x'),
                "y": request.query_params.get('y')
            }}
            kid = verify_signature_softhsm2()
            signatures = request.query_params.get('signatures')
            if kid is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print("ERROR:", e)
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={kid}, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='POST', manual_parameters=[sw_accessToken_code, sw_kid_code], responses=post_response)
    @action(methods=['POST'], detail=False, url_path='gen-key')
    def gen_key_from_softhsm2(self, request):
        try:
            accessToken = request.query_params.get('accessToken')
            kid = request.query_params.get('kid')
            kid = gen_key_softhsm2()
            if kid is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print("ERROR:", e)
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={kid}, status=status.HTTP_200_OK)
        return Response({"result":kid})
    