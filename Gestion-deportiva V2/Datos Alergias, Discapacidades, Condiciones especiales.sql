-- Insertar datos en la tabla Allergies
INSERT INTO "allergies" (allergie_name, description)
VALUES
    ('Polen', 'Alergia al polen que puede afectar el rendimiento durante la primavera.'),
    ('Lácteos', 'Intolerancia a los lácteos que podría requerir una dieta específica.'),
    ('Ejercicio Intenso', 'Sensibilidad a ejercicios intensos que requiere precauciones.'),
    ('Mariscos', 'Alergia a los mariscos que puede limitar las opciones de alimentación.'),
    ('Hierba', 'Alergia a la hierba que puede afectar la práctica al aire libre.');

-- Insertar datos en la tabla disabilities
INSERT INTO "disabilities" (disability_name, description)
VALUES
    ('Discapacidad Visual', 'Limitación en la visión que podría requerir adaptaciones.'),
    ('Discapacidad Motora', 'Dificultades en la movilidad que requieren atención especial.'),
    ('Asma', 'Problemas respiratorios como el asma que podrían afectar el rendimiento.'),
    ('Lesiones Previas', 'Lesiones pasadas que requieren precauciones durante la actividad física.'),
    ('Sensibilidad al Calor', 'Sensibilidad al calor que necesita hidratación y pausas regulares.');

-- Insertar datos en la tabla specialCon
insert into "specialConditions" ("specialConditions_name", "description")
VALUES
    ('Diabetes', 'Gestión de niveles de azúcar y planificación de comidas.'),
    ('Hipertensión', 'Control de la presión arterial durante la actividad física.'),
    ('Asma', 'Manejo de problemas respiratorios y alergias.'),
    ('Enfermedades Cardiovasculares', 'Cuidado del corazón y prevención de exceso de esfuerzo.'),
    ('Epilepsia', 'Consideraciones para prevenir convulsiones durante la actividad.');

SELECT * FROM "specialConditions"
