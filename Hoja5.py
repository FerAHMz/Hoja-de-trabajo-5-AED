import simpy
import random

def proceso(env, nombre, cpu, memoria, cantidad_memoria, total_instrucciones, velocidad_cpu):
    print(f'{env.now}: El proceso {nombre} ha sido creado, estado: "new"')
    yield memoria.get(cantidad_memoria)
    print(f'{env.now}: El proceso {nombre} está listo, estado: "ready"')
    
    while total_instrucciones > 0:
        with cpu.request() as req:
            yield req
            instrucciones_ejecutadas = min(total_instrucciones, velocidad_cpu)
            total_instrucciones -= instrucciones_ejecutadas
            yield env.timeout(1)
            print(f'{env.now}: El proceso {nombre} está en ejecución, estado: "running"')
            
            if total_instrucciones > 0:
                if random.random() < 0.1:  # Asumiendo un 10% de probabilidad para E/S
                    print(f'{env.now}: El proceso {nombre} está en espera (I/O), estado: "waiting"')
                    yield env.timeout(2)  # Espera de E/S

    print(f'{env.now}: El proceso {nombre} ha terminado, estado: "terminated"')
    yield memoria.put(cantidad_memoria)

def configuracion_simulacion(env, num_procesos, intervalo, capacidad_memoria, velocidad_cpu, num_cpus):
    cpu = simpy.Resource(env, capacity=num_cpus)
    memoria = simpy.Container(env, init=capacidad_memoria, capacity=capacidad_memoria)

    for i in range(num_procesos):
        tiempo_llegada = random.expovariate(1.0 / intervalo)
        env.process(proceso(env, f'Proceso {i}', cpu, memoria, 10, 10, velocidad_cpu))
        yield env.timeout(tiempo_llegada)

# Parámetros de la simulación
env = simpy.Environment()
env.process(configuracion_simulacion(env, num_procesos=5, intervalo=10, capacidad_memoria=100, velocidad_cpu=3, num_cpus=2))
env.run(until=50)

