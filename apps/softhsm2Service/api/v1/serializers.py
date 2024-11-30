from rest_framework.serializers import ModelSerializer
from ...models import genKey_SoftHSM

class SoftHSmSerializer(ModelSerializer):
    class Meta:
        model = genKey_SoftHSM
        fields = '__all__'