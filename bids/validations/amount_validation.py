from rest_framework.response import Response
from rest_framework import status

def validate_amount(amount) :
     if not amount:
        return Response({
            "error": "amount field is required"
        },status=status.HTTP_400_BAD_REQUEST)