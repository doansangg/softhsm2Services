from django.db import models

# Create your models here.

class genKey_SoftHSM(models.Model):
    accessToken = models.TextField()
    expirationTime = models.IntegerField(default = 0)
    signatureAlgorithm = models.CharField(max_length=20)
    kty = models.CharField(max_length=20)
    kid = models.CharField(max_length=20)
    use = models.CharField(max_length=20)
    alg = models.CharField(max_length=20)
    crv = models.CharField(max_length=20)
    exp = models.CharField(max_length=20)
    #height = models.FloatField(default=0)
    #weight = models.FloatField(default = 0)
    def __str__(self):
        return self.accessToken

class signature_SoftHSM(models.Model):
    accessToken = models.TextField()
    signingInput = models.TextField()
    signatureAlgorithm = models.CharField(max_length=20)
    alias = models.CharField(max_length=20)
    sig = models.TextField()
    def __str__(self):
        return self.accessToken
    
class verifySignature_SoftHSM(models.Model):
    accessToken = models.TextField()
    signingInput = models.TextField()
    signatureAlgorithm = models.CharField(max_length=20)
    alias = models.CharField(max_length=20)
    alg = models.CharField(max_length=20)
    kid = models.CharField(max_length=20)
    use = models.CharField(max_length=20)
    kty = models.CharField(max_length=20)
    n = models.TextField()
    e = models.TextField()
    signature = models.TextField()
    def __str__(self):
        return self.accessToken