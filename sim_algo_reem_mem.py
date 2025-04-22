#!/usr/bin/env python

# marcos_libres = [0x0,0x1,0x2]
# reqs = [ 0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1, 0x0B, 0xDF, 0x0A ]
# segmentos =[ ('.text', 0x00, 0x1A),
#              ('.data', 0x40, 0x28),
#              ('.heap', 0x80, 0x1F),
#              ('.stack', 0xC0, 0x22),
#             ]
import collections
def procesar(segmentos, reqs, marcos_libres):
    # Implemente esta funcion
    PAGE_SIZE = 0x10
    SEG_FAULT_ADDR = 0x1ff
    page_table = {}
    frame_to_page = {}
    lru_order = collections.deque()
    free_frames = sorted(list(marcos_libres))
    results = []
    for req in reqs:
        segmento_valido = False
        for _, base, limite in segmentos:
            if base <= req < (base + limite):
                segmento_valido = True
                break
        if not segmento_valido:
            results.append((req, SEG_FAULT_ADDR, "Segmentation Fault"))
            break
        page_num = req // PAGE_SIZE
        offset = req % PAGE_SIZE
        if page_num in page_table:
            frame_num = page_table[page_num]
            direccion_fisica = frame_num * PAGE_SIZE + offset
            accion = "Marco ya estaba asignado"
            lru_order.remove(page_num)
            lru_order.append(page_num)
            results.append((req, direccion_fisica, accion))
        else:
            if free_frames:
                frame_num = free_frames.pop()
                accion = "Marco libre asignado"
                page_table[page_num] = frame_num
                frame_to_page[frame_num] = page_num
                lru_order.append(page_num)

                direccion_fisica = frame_num * PAGE_SIZE + offset
                results.append((req, direccion_fisica, accion))
            else:
                if not lru_order:
                    pass
                accion = "Marco asignado"
                victim_page_num = lru_order.popleft()
                victim_frame_num = page_table.pop(victim_page_num)
                del frame_to_page[victim_frame_num]
                frame_num = victim_frame_num
                page_table[page_num] = frame_num
                frame_to_page[frame_num] = page_num
                lru_order.append(page_num)

                direccion_fisica = frame_num * PAGE_SIZE + offset
                results.append((req, direccion_fisica, accion))

    return results
    
def print_results(results):
    for result in results:
        print(f"Req: {result[0]:#0{4}x} Direccion Fisica: {result[1]:#0{5}x} Acción: {result[2]}")

if __name__ == '__main__':
    results = procesar(segmentos, reqs, marcos_libres)
    print_results(results)

