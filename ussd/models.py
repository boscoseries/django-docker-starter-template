import uuid
from django.db import models


# Create your models here.
class USSD(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at', )

    def __str__(self):
        return self.value
