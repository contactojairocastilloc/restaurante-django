"""Formatos numéricos y de fecha para Chile.

Django no incluye el locale es_CL, así que al usar LANGUAGE_CODE = 'es-cl'
cae en 'es' (España), que separa los miles con un espacio: 9 990.
En Chile se usa el punto: 9.990. Este módulo corrige eso.
"""

DECIMAL_SEPARATOR = ','
THOUSAND_SEPARATOR = '.'
NUMBER_GROUPING = 3

DATE_FORMAT = 'd/m/Y'
DATETIME_FORMAT = 'd/m/Y H:i'
SHORT_DATE_FORMAT = 'd/m/Y'
