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

def delete_product(product_id) :
    product = Product.objects.get(id=product_id) 
    product.delete()
    return Response({"message :":f"product with ID : {product_id} deleted"})

def get_product_by_id(product_id) :
    try :
        product = Product.objects.get(id=product_id) 
        return Response({"data":product}, status=200)
    except Product.DoesNotExist :
        return Response({"error":"product with ID : {product_id} is not available"}) 