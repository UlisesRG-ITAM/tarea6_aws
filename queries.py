QUERY = '''
    SELECT inf.fecha, inf.inflacion_inpc, cam.tipo_cambio, int.cetes_365
    FROM "econ"."inflacion" as inf
    INNER JOIN "econ"."tipo_de_cambio" as cam
    ON inf.fecha = cam.fecha
    INNER JOIN "econ"."tasa_de_interes" as int
    ON inf.fecha = int.fecha;
'''