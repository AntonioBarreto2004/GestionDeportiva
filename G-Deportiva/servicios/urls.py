from django.urls import path
from servicios.Controllers import viewsFactura
from servicios.Controllers import viewsReciboPago
from servicios.Controllers import viewsServices

urlpatterns = [
    path('list-services/', viewsServices.get_servicio, name='list Services'),
    path('create-services/', viewsServices.create_servicio, name='create Services'),
    path('update-services/', viewsServices.update_servicio, name='update Services'),
    path('delete-services/', viewsServices.delete_servicio, name='delete Services'),
    
    path('list-recibo-Pago/', viewsReciboPago.get_recibo_pago, name='list Recibo Pago'),
    path('create-recibo-Pago/', viewsReciboPago.create_recibo_pago, name='create Recibo Pago'),
    path('update-recibo-Pago/', viewsReciboPago.update_recibo_pago, name='Update Recibo Pago'),
    path('delete-recibo-Pago/', viewsReciboPago.delete_recibo_pago, name='delete Recibo Pago'),

    path('factura-pdf/<int:pk>/', viewsFactura.download_pdf_recibo_pago, name='Factura PDF'),
    path('factura-excel/<int:pk>/', viewsFactura.download_excel_recibo_pago, name='Factura EXCEL'),

]