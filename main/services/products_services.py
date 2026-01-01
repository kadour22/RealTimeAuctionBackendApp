from rest_framework.response import Response
from rest_framework import status 
from main.models import Product

def create_product(name, price, image, description) :
    product = Product.objects.create(
        name        = name,
        price       = price,
        description = description,
        image       = image
    )
    return Response(
        product , status=201
    )