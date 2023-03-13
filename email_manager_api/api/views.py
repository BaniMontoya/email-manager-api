from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Correo, Empresa
from .serializers import CorreoSerializer


class RegistraCorreoAPIView(APIView):
    def post(self, request, format=None):
        # Deserialize the request data with CorreoSerializer
        serializer = CorreoSerializer(data=request.data)
        
        # Check if the deserialized data is valid
        if serializer.is_valid():
            # Get the 'empresa_emisora' field from the validated data
            empresa_emisora = serializer.validated_data['empresa_emisora']
            
            # Try to get the corresponding Empresa object from the database
            try:
                empresa = Empresa.objects.get(nombre=empresa_emisora)
            except Empresa.DoesNotExist:
                # If the Empresa object doesn't exist, return a 400 Bad Request response
                return Response({'error': 'The sender company of the email is not in our catalog of known companies'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Save the Correo object with the Empresa object as the 'empresa_emisora' field
            correo = serializer.save(empresa_emisora=empresa)
            
            # Return a 201 Created response with the ID of the saved Correo object
            return Response({'id': correo.id}, status=status.HTTP_201_CREATED)
        
        # If the deserialized data is not valid, return a 400 Bad Request response with the validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BuscarCorreoAPIView(APIView):
    def get(self, request, format=None):
        # Get the search parameters from the GET request query parameters
        contenido = request.query_params.get('contenido', None)
        empresa_emisora = request.query_params.get('empresa_emisora', None)
        empresa_destinataria = request.query_params.get('empresa_destinataria', None)
        fecha_desde = request.query_params.get('fecha_desde', None)
        fecha_hasta = request.query_params.get('fecha_hasta', None)

        # Perform the corresponding search in the database
        correos = Correo.objects.all()
        if contenido:
            correos = correos.filter(contenido__icontains=contenido)
        if empresa_emisora:
            correos = correos.filter(empresa_emisora__nombre__icontains=empresa_emisora)
        if empresa_destinataria:
            correos = correos.filter(empresa_destinataria__nombre__icontains=empresa_destinataria)
        if fecha_desde:
            correos = correos.filter(fecha__gte=fecha_desde)
        if fecha_hasta:
            correos = correos.filter(fecha__lte=fecha_hasta)

        # Paginate the search results with a page size of 10
        paginator = Paginator(correos, 10)
        page_number = request.query_params.get('page')
        page = paginator.get_page(page_number)
        serializer = CorreoSerializer(page, many=True)

        # Return the paginated results to the client
        return Response(serializer.data)
