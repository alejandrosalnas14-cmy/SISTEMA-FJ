from modelos import Cliente, ReservaSala, AlquilerEquipos, AsesoriaEspecializada, Reserva
from excepciones import SoftwareFJError
from logger import LoggerFJ

def ejecutar_simulacion():
    print("==================================================")
    print(" INICIO DE SIMULACIÓN - SISTEMA SOFTWARE FJ")
    print("==================================================")
    
    lista_clientes = []
    lista_servicios = []
    lista_reservas = []

    # OPERACIÓN 1: Registro válido de un cliente
    print("\n--- Operación 1: Registro Válido de Cliente ---")
    try:
        c1 = Cliente("C001", "Barbara Rojas", "Barbara.Rojas@softwarefj.com", "3228466208")
        lista_clientes.append(c1)
        print(f"[OK] Creado: {c1}")
        LoggerFJ.info(f"Operación 1 exitosa: {c1.identificador}")
    except SoftwareFJError as e:
        LoggerFJ.error(f"Operación 1 fallida: {e}")
    finally:
        print("[FIN] Bloque try/except/finally completado para Op 1.")

    # OPERACIÓN 2: Registro inválido de cliente
    print("\n--- Operación 2: Registro Inválido de Cliente (Email Erróneo) ---")
    try:
        c_invalido = Cliente("C002", "Carlos Pineda", "carlos-sin-arroba.com", "3188838378")
        lista_clientes.append(c_invalido)
    except SoftwareFJError as e:
        print(f"[CAPT_EXC] Excepción atrapada correctamente: {e} (Código: {e.codigo_error})")
        LoggerFJ.advertencia(f"Operación 2 controlada: {e}")
    else:
        print("[INFO] El cliente se creó sin novedad.")

    # OPERACIÓN 3: Creación correcta de un servicio (Reserva de Sala)
    print("\n--- Operación 3: Creación Correcta de Servicio (Sala) ---")
    try:
        s1 = ReservaSala("S001", tarifa_base=40.0, capacidad=15, recursos_extra=True)
        lista_servicios.append(s1)
        print(f"[OK] Servicio creado: {s1.describir()} - Tarifa base: ${s1.tarifa_base}")
    except SoftwareFJError as e:
        LoggerFJ.error(f"Op 3 error: {e}")

    # OPERACIÓN 4: Creación incorrecta de servicio (Tarifa negativa)
    print("\n--- Operación 4: Creación Incorrecta de Servicio (Tarifa Negativa) ---")
    try:
        s_mal = AlquilerEquipos("S002", tarifa_base=-15.0, tipo_equipo="Servidor Grafico")
        lista_servicios.append(s_mal)
    except SoftwareFJError as e:
        print(f"[CAPT_EXC] Excepción controlada en tarifa: {e}")
        LoggerFJ.advertencia(f"Op 4 controlada: {e}")

    # OPERACIÓN 5: Creación de servicios adicionales
    print("\n--- Operación 5: Creación de Servicios Adicionales ---")
    try:
        s2 = AlquilerEquipos("S003", tarifa_base=25.0, tipo_equipo="MacBook Pro", seguro_incluido=True)
        s3 = AsesoriaEspecializada("S004", tarifa_base=80.0, nivel_experticia="senior")
        lista_servicios.extend([s2, s3])
        print(f"[OK] Creados servicios: {s2.describir()} y {s3.describir()}")
    except SoftwareFJError as e:
        LoggerFJ.error(f"Op 5 error: {e}")

    # OPERACIÓN 6: Creación de un segundo cliente válido
    print("\n--- Operación 6: Registro de Segundo Cliente Válido ---")
    try:
        c2 = Cliente("C003", "Carmen", "Carmenz@gmail.com", "3142547718")
        lista_clientes.append(c2)
        print(f"[OK] Creado: {c2}")
    except SoftwareFJError as e:
        LoggerFJ.error(f"Op 6 error: {e}")

    # OPERACIÓN 7: Creación exitosa de una Reserva y cálculo
    print("\n--- Operación 7: Creación de Reserva Exitosa y Cálculo ---")
    try:
        res1 = Reserva("R001", cliente=lista_clientes[0], servicio=lista_servicios[0], duracion_horas=4.0)
        lista_reservas.append(res1)
        res1.confirmar()
        
        costo_base = res1.calcular_total_pago()
        costo_con_desc = res1.calcular_total_pago(descuento_porcentaje=10.0)
        costo_total_final = res1.calcular_total_pago(descuento_porcentaje=10.0, incluir_impuesto=True)
        
        print(f"[OK] Reserva {res1.identificador} creada para {res1.cliente.nombre}.")
        print(f"     Costo Base: ${costo_base:.2f}")
        print(f"     Con 10% Descuento: ${costo_con_desc:.2f}")
        print(f"     Total Final (Desc + IVA 19%): ${costo_total_final:.2f}")
    except SoftwareFJError as e:
        LoggerFJ.error(f"Op 7 error: {e}")

    # OPERACIÓN 8: Intento de reserva con duración inválida
    print("\n--- Operación 8: Intento de Reserva con Duración Inválida ---")
    try:
        res_fallida = Reserva("R002", cliente=lista_clientes[1], servicio=lista_servicios[2], duracion_horas=500.0)
    except SoftwareFJError as e:
        print(f"[CAPT_EXC] Excepción de duración capturada: {e} (Código: {e.codigo_error})")
        LoggerFJ.advertencia(f"Op 8 controlada: {e}")

    # OPERACIÓN 9: Segunda reserva exitosa
    print("\n--- Operación 9: Segunda Reserva Exitosa (Asesoría Senior) ---")
    try:
        res2 = Reserva("R003", cliente=lista_clientes[1], servicio=lista_servicios[2], duracion_horas=3.0)
        lista_reservas.append(res2)
        res2.confirmar()
        costo_asesoria = res2.calcular_total_pago()
        print(f"[OK] Reserva {res2.identificador} confirmada. Servicio: {res2.servicio.describir()}")
        print(f"     Costo total asesoría: ${costo_asesoria:.2f}")
    except SoftwareFJError as e:
        LoggerFJ.error(f"Op 9 error: {e}")

    # OPERACIÓN 10: Cancelación de reserva
    print("\n--- Operación 10: Cancelación de Reserva y Cierre de Ciclo ---")
    try:
        target_reserva = lista_reservas[0]
        print(f"Estado previo de {target_reserva.identificador}: {target_reserva.estado}")
        target_reserva.cancelar()
        print(f"Estado posterior de {target_reserva.identificador}: {target_reserva.estado}")
        print("[OK] El sistema continúa operando sin interrupciones tras la cancelación.")
        LoggerFJ.info("Operación 10 completada: Simulación finalizada de forma estable.")
    except Exception as e:
        LoggerFJ.error(f"Op 10 error crítico: {e}")

    print("\n==================================================")
    print(" SIMULACIÓN FINALIZADA CON ÉXITO")
    print(" Revise el archivo 'sistema_fj.log' para ver el registro.")
    print("==================================================")

if __name__ == "__main__":
    ejecutar_simulacion()
