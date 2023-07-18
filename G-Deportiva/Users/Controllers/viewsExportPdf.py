from reportlab.lib import colors
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
from reportlab.lib.units import inch
from rest_framework.decorators import api_view
from ..models import *
from ..serializers import *


@api_view(['GET'])
def export_users_to_pdf(request):
    id = request.GET.get('id')
    email = request.GET.get('email')
    name = request.GET.get('name')
    last_name = request.GET.get('last_name')
    cod_rol = request.GET.get('cod_rol')
    last_name = request.GET.get('last_name')
    last_name = request.GET.get('last_name')
    queryset = User.objects.all()
    if email:
        queryset = queryset.filter(email=email)
    if name:
        queryset = queryset.filter(name=name)
    if last_name:
        queryset = queryset.filter(last_name=last_name)
    if cod_rol:
        queryset = queryset.filter(cod_rol=cod_rol)
    if id:
        queryset = queryset.filter(id=id)
    # Agrega aquí los demás filtros según los campos que deseas filtrar

    serializer = UserSerializer(queryset, many=True)

    # Obtener los datos serializados
    datos = serializer.data

    # Crear la respuesta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="lista-usuarios.pdf"'

    # Crear el documento PDF
    buffer_pdf = io.BytesIO()
    pdf = SimpleDocTemplate(buffer_pdf, pagesize=letter)

    # Crear el contenido del PDF
    contenido = []

    # Establecer estilos de párrafo
    estilos = getSampleStyleSheet()
    estilo_encabezado = estilos['Heading2']
    estilo_celda = estilos['BodyText']

    # Agregar los datos a la tabla para cada usuario
    for dato in datos:
        # Crear una lista de filas para el usuario actual
        filas_usuario = []

        for clave, valor in dato.items():
            if clave == 'cod_rol':
                try:
                    rol_id = valor
                    rol = Rol.objects.get(id=rol_id)
                    valor = rol.name_rol
                except Rol.DoesNotExist:
                    valor = ''  # Si el rol no existe, asignar un valor vacío
            elif clave == 'type_document':
                try:
                    type_document_id = valor
                    type_document = DocumentType.objects.get(id=type_document_id)
                    valor = type_document.name
                except DocumentType.DoesNotExist:
                    valor = ''  # Si el tipo de documento no existe, asignar un valor vacío
            elif clave == 'gender_user':
                try:
                    gender_id = valor
                    gender_n = gender.objects.get(id=gender_id)
                    valor = gender_n.name_gender
                except gender.DoesNotExist:
                    valor = ''  # Si el tipo de documento no existe, asignar un valor vacío

            encabezado = Paragraph(clave, estilo_encabezado)
            celda = Paragraph(str(valor), estilo_celda)
            filas_usuario.append([encabezado, celda])

        # Crear la tabla para el usuario actual
        tabla_usuario = Table(filas_usuario, colWidths=[200, 200])  # Ajustar el ancho de las columnas según tus necesidades

        # Establecer estilo de la tabla para el usuario actual
        estilo_tabla = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        # Aplicar el estilo a la tabla
        tabla_usuario.setStyle(estilo_tabla)

        # Agregar la tabla del usuario actual al contenido del PDF
        contenido.append(tabla_usuario)
        contenido.append(Spacer(1, 0.2 * inch))  # Agregar espacio entre tablas

    # Generar el PDF con todas las tablas
    pdf.build(contenido)

    buffer_pdf.seek(0)
    response.write(buffer_pdf.getvalue())

    return response