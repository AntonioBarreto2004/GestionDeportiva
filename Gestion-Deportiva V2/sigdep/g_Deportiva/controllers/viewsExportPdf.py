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
    filters = {
        'id': request.GET.get('id'),
        'email': request.GET.get('email'),
        'name': request.GET.get('name'),
        'last_name': request.GET.get('last_name'),
        'cod_rol': request.GET.get('cod_rol'),
    }

    people_queryset = People.objects.all()

    for field, value in filters.items():
        if value:
            filter_kwargs = {f'{field}__icontains': value}
            people_queryset = people_queryset.filter(**filter_kwargs)

    people_queryset = people_queryset.prefetch_related('user_set', 'user_set__rol')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="lista-usuarios.pdf"'

    buffer_pdf = io.BytesIO()
    pdf = SimpleDocTemplate(buffer_pdf, pagesize=letter)
    contenido = []

    estilos = getSampleStyleSheet()
    estilo_encabezado = estilos['Heading2']
    estilo_celda = estilos['BodyText']

    for person in people_queryset:
        datos_persona = []
        # Título como la primera celda de la tabla de datos de persona
        titulo_persona = f'Datos de {person.name} {person.last_name}'
        datos_persona.append([titulo_persona, ''])
        
        for field in person._meta.fields:
            if field.name != 'id':
                datos_persona.append([field.verbose_name, str(getattr(person, field.name))])

        tabla_persona = Table(datos_persona, colWidths=[200, 200])
        estilo_tabla_persona = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#CCCCCC'),
            ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), '#EEEEEE'),
            ('GRID', (0, 0), (-1, -1), 1, '#000000'),
        ])
        tabla_persona.setStyle(estilo_tabla_persona)
        contenido.append(tabla_persona)
        contenido.append(Spacer(1, 0.2 * inch))

        usuarios_relacionados = person.user_set.all()
        if usuarios_relacionados:
            for user in usuarios_relacionados:
                datos_usuario = []
                # Título como la primera celda de la tabla de datos de usuario relacionado
                titulo_usuario = f'Datos de usuario relacionado'
                datos_usuario.append([titulo_usuario, ''])
                
                for field in user._meta.fields:
                    if field.name != 'id' and field.name != 'password':
                        valor = get_related_name_or_empty(Rol, getattr(user, field.name)) if field.name == 'rol_id' else getattr(user, field.name)
                        datos_usuario.append([field.verbose_name, str(valor)])
                tabla_usuario = Table(datos_usuario, colWidths=[200, 200])
                estilo_tabla_usuario = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), '#CCCCCC'),
                    ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), '#EEEEEE'),
                    ('GRID', (0, 0), (-1, -1), 1, '#000000'),
                ])
                tabla_usuario.setStyle(estilo_tabla_usuario)
                contenido.append(tabla_usuario)
                contenido.append(Spacer(1, 0.2 * inch))

    pdf.build(contenido)
    buffer_pdf.seek(0)
    response.write(buffer_pdf.getvalue())
    return response

def get_related_name_or_empty(model, id):
    try:
        instance = model.objects.get(id=id)
        return instance.name
    except model.DoesNotExist:
        return ''



