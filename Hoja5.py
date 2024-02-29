import simpy  # Importa el módulo simpy para la simulación de eventos discretos.
import random  # Importa el módulo random para generar números aleatorios.
import statistics

tiempos_inicio = {}  # Almacena el tiempo de inicio de cada proceso
tiempos_fin = {}  # Almacena el tiempo de finalización de cada proceso

# Definición de la función proceso, que simula las acciones de un proceso en el sistema.
def proceso(env, nombre, cpu, memoria, cantidad_memoria, total_instrucciones, velocidad_cpu):
    tiempo_inicio = env.now  # Registrar el tiempo de inicio
    print(f'{tiempo_inicio}: El proceso {nombre} ha sido creado, tiempo inicial.')
    tiempos_inicio[nombre] = env.now  # Almacena el tiempo de inicio del proceso
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
    tiempos_fin[nombre] = env.now  # Almacena el tiempo de finalización del proceso
    yield memoria.put(cantidad_memoria)
    
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

def calcular_estadisticas():
    tiempos_totales = [tiempos_fin[nombre] - tiempos_inicio[nombre] for nombre in tiempos_inicio]
    print(f"Tiempo promedio de ejecución: {statistics.mean(tiempos_totales):.2f}")
    if len(tiempos_totales) > 1:
        print(f"Desviación estándar: {statistics.stdev(tiempos_totales):.2f}")
    else:
        print("Desviación estándar: No aplicable con un solo proceso.")

# Configura y ejecuta el entorno de simulación con los parámetros definidos.
env = simpy.Environment()
env.process(configuracion_simulacion(env, num_procesos=5, intervalo=10, capacidad_memoria=100, velocidad_cpu=3, num_cpus=2))
env.run(until=50)
calcular_estadisticas()