from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Positions)
class CpositionsAdmin(admin.ModelAdmin):
    list_display = ['at_position', 'at_positiona']
    search_fields = ['at_position']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['t_name', 'c_name']
    search_fields = ['t_name']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['team_name', 'team_category', 'team_image']
    search_fields = ['team_name']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'team_category':
            # Filtrar las categorías disponibles en función del deporte seleccionado
            kwargs['queryset'] = Category.objects.filter(t_name=request.GET.get('t_name'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ['dorsal',  'a_category', 'at_team', 'c_position', 'c_positiona', 'at_technicalv', 'at_tacticalv', 'at_physicalv']
    search_fields = ['at_user']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'at_team':
            # Filtrar los equipos disponibles en función del deporte seleccionado
            category_id = request.GET.get('a_category')
            if category_id:
                kwargs['queryset'] = Team.objects.filter(Category_team__id=category_id)
            else:
                kwargs['queryset'] = Team.objects.none()
        elif db_field.name in ['c_position', 'c_positiona']:
            # Filtrar las posiciones disponibles en función del equipo seleccionado
            team_id = request.GET.get('at_team')
            if team_id:
                kwargs['queryset'] = Positions.objects.filter(team__id=team_id)
            else:
                kwargs['queryset'] = Positions.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Anthropometric)
class AnthropometricAdmin(admin.ModelAdmin):
    list_display = ['athlete_id', 'atpt_controlDate', 'atpt_arm', 'atpt_chest', 'atpt_hip', 'atpt_calf', 'atpt_humerus', 'atpt_femur', 'atpt_wrist', 'atpt_triceps', 'atpt_suprailiac', 
                    'atpt_pectoral', 'atpt_height', 'atpt_weight', 'atpt_bmi', 'atpt_created_date', 'atpt_updated_date']








