import simpy  # Importa el módulo simpy para la simulación de eventos discretos.
import random  # Importa el módulo random para generar números aleatorios.

# Definición de la función proceso, que simula las acciones de un proceso en el sistema.
def proceso(env, nombre, cpu, memoria, cantidad_memoria, total_instrucciones, velocidad_cpu):
    tiempo_inicio = env.now  # Registrar el tiempo de inicio
    print(f'{tiempo_inicio}: El proceso {nombre} ha sido creado, tiempo inicial.')
    yield memoria.get(cantidad_memoria)

    while total_instrucciones > 0:
        with cpu.request() as req:
            yield req
            instrucciones_ejecutadas = min(total_instrucciones, velocidad_cpu)
            total_instrucciones -= instrucciones_ejecutadas
            yield env.timeout(1)

            if total_instrucciones > 0 and random.random() < 0.1:
                yield env.timeout(2)  # Espera de E/S

    tiempo_final = env.now  # Registrar el tiempo de finalización
    print(f'{tiempo_final}: El proceso {nombre} ha terminado, tiempo final.')
    print(f"El proceso {nombre} inició en {tiempo_inicio} y terminó en {tiempo_final}.")
    yield memoria.put(cantidad_memoria)
    # pedir permiso escribir -- list
    # escribe en el list

    
    # Mientras el proceso tenga instrucciones por ejecutar, sigue en un ciclo.
    while total_instrucciones > 0:
        # Solicita acceso al CPU.
        with cpu.request() as req:
            yield req
            # Calcula el número de instrucciones ejecutadas en este ciclo.
            instrucciones_ejecutadas = min(total_instrucciones, velocidad_cpu)
            total_instrucciones -= instrucciones_ejecutadas
            # Simula el tiempo de ejecución de las instrucciones.
            yield env.timeout(1)
            # Imprime un mensaje indicando que el proceso está en ejecución.
            print(f'{env.now}: El proceso {nombre} está en ejecución, estado: "running"')
            
            # Si aún quedan instrucciones por ejecutar, verifica si el proceso entra en espera por E/S.
            if total_instrucciones > 0:
                if random.random() < 0.1:  # 10% de probabilidad de necesitar E/S.
                    # Imprime un mensaje indicando que el proceso espera por E/S.
                    print(f'{env.now}: El proceso {nombre} está en espera (I/O), estado: "waiting"')
                    yield env.timeout(2)  # Simula el tiempo de espera por E/S.

    # Una vez completadas todas las instrucciones, imprime un mensaje indicando que el proceso ha terminado.
    print(f'{env.now}: El proceso {nombre} ha terminado, estado: "terminated"')
    # Devuelve la memoria utilizada al contenedor de memoria.
    yield memoria.put(cantidad_memoria)

# Define la función de configuración de la simulación.
def configuracion_simulacion(env, num_procesos, intervalo, capacidad_memoria, velocidad_cpu, num_cpus):
    # Crea recursos de CPU y memoria con capacidades definidas.
    cpu = simpy.Resource(env, capacity=num_cpus)
    memoria = simpy.Container(env, init=capacidad_memoria, capacity=capacidad_memoria)

    # Inicia procesos en intervalos aleatorios.
    for i in range(num_procesos):
        tiempo_llegada = random.expovariate(1.0 / intervalo)
        env.process(proceso(env, f'Proceso {i}', cpu, memoria, 10, 10, velocidad_cpu))
        yield env.timeout(tiempo_llegada)

# Configura y ejecuta el entorno de simulación con los parámetros definidos.
env = simpy.Environment()
env.process(configuracion_simulacion(env, num_procesos=5, intervalo=10, capacidad_memoria=100, velocidad_cpu=3, num_cpus=2))
env.run(until=50)
