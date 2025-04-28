#!/usr/bin/env python
'''
marcos_libres = [0x0,0x1,0x2]
reqs = [ 0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1, 0x0B, 0xDF, 0x0A ]
segmentos =[ ('.text', 0x00, 0x1A),
            ('.data', 0x40, 0x28),
            ('.heap', 0x80, 0x1F),
            ('.stack', 0xC0, 0x22),
            ]
'''
def procesar(segmentos, reqs, marcos_libres):
    page_size = 16
    n = len(reqs)
    m = len(segmentos)
    tabla_paginas = {}
    estados_marcos = {}
    cola_marcos = []
    marcos_disponibles = list(marcos_libres)
    accion = ""
    results = []
    physical_direction = None

    for i in range(n):
        finished = False
        for j in range(m):
            if(segmentos[j][1] <= reqs[i] < segmentos[j][1] + segmentos[j][2]):
                finished = True
                break

        if(finished == False):
            accion = "Segmentation Fault"
            physical_direction = 0x1FF
            results.append((reqs[i], physical_direction, accion))
            break

        numero_pagina_logica = reqs[i] // page_size
        offset = reqs[i] % page_size

        if numero_pagina_logica in tabla_paginas:
            accion = "Marco ya estaba asignado"
            marco_fisico_actual = tabla_paginas[numero_pagina_logica]
            cola_marcos.remove(marco_fisico_actual)
            cola_marcos.append(marco_fisico_actual)
            physical_direction = (marco_fisico_actual * page_size) + offset

        else:
            if len(cola_marcos) < len(marcos_libres):
                accion = "Marco libre asignado"
                marco_fisico_asignado = marcos_disponibles.pop(0)
                tabla_paginas[numero_pagina_logica] = marco_fisico_asignado
                estados_marcos[marco_fisico_asignado] = numero_pagina_logica
                cola_marcos.append(marco_fisico_asignado)
                physical_direction = (marco_fisico_asignado * page_size) + offset

            else:
                accion = "Marco asignado"
                marco_lru = cola_marcos.pop(0)
                pagina_desalojada = estados_marcos.pop(marco_lru)
                del tabla_paginas[pagina_desalojada]
                marco_fisico_asignado = marco_lru
                tabla_paginas[numero_pagina_logica] = marco_fisico_asignado
                estados_marcos[marco_fisico_asignado] = numero_pagina_logica
                cola_marcos.append(marco_fisico_asignado)
                physical_direction = (marco_fisico_asignado * page_size) + offset

        results.append((reqs[i], physical_direction, accion))

    return results

    
def print_results(results):
    for result in results:
        print(f"Req: {result[0]:#0{4}x} Direccion Fisica: {result[1]:#0{4}x} Acción: {result[2]}")

if __name__ == '__main__':
    results = procesar(segmentos, reqs, marcos_libres)
    print_results(results)
