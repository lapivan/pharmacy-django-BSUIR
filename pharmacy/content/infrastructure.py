from concurrent.futures import ProcessPoolExecutor
import math
import time
import random
import threading
import asyncio

class Infrastructure:
    @staticmethod
    def move_players(lock, coords_list, player: int, steps: int=10, delay: float=0.05, thread_logs=None) -> None:
        if thread_logs is not None:
            thread_logs.append(f"Поток: Игрок {player+1} начал движение.")
            
        for _ in range(steps):
            time.sleep(delay)
            with lock:
                coords_list[player][0] += random.randint(-1, 1)
                coords_list[player][1] += random.randint(-1, 1)
        
        if thread_logs is not None:
            thread_logs.append(f"Поток: Игрок {player+1} закончил движение.")

    @staticmethod
    def run_threading_test():
        coords_lock = threading.Lock()
        coords_list = [[random.randint(-10, 10), random.randint(-10, 10)] for _ in range(5)]
        logs = []
        logs.append("Начинаем последовательное движение.")
        start_seq = time.perf_counter()
        for player in range(5):
            logs.append(f"Двигаем игрока {player+1}.")
            Infrastructure.move_players(coords_lock, coords_list, player, 10, 0.05)
        duration_seq = time.perf_counter() - start_seq
        logs.append(f"Последовательное выполнение завершено за: {duration_seq:.4f} секунд.")
        logs.append("\nНачинаем многопоточное движение.")
        threads = []
        thread_messages = []
        start_threads = time.perf_counter()
        for i in range(5):
            t = threading.Thread(
                target=Infrastructure.move_players, 
                args=(coords_lock, coords_list, i, 10, 0.05, thread_messages)
            )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        duration_threads = time.perf_counter() - start_threads
        logs.extend(thread_messages)
        logs.append(f"Многопоточное выполнение завершено за: {duration_threads:.4f} секунд.")
        return {
            'logs': "\n".join(logs),
            'seq_time': round(duration_seq, 4),
            'parallel_time': round(duration_threads, 4)
        }
    
    @staticmethod
    def calculate_collision_vector(obj_data):
        x, y, mass, velocity = obj_data
        for _ in range(100):
            angle = math.atan2(y, x)
            force = mass * (velocity ** 2) / 2
            x = math.cos(angle) * force
            y = math.sin(angle) * force
        return (x, y)

    @staticmethod
    def run_multiprocessing_test():
        num_objects = 100000
        data = [
            (random.uniform(-100, 100), random.uniform(-100, 100), 
             random.uniform(1, 10), random.uniform(1, 50)) 
            for _ in range(num_objects)
        ]
        logs = []
        logs.append(f"Расчет {num_objects} векторов.")
        start_seq = time.perf_counter()
        _ = [Infrastructure.calculate_collision_vector(obj) for obj in data]
        duration_seq = time.perf_counter() - start_seq
        logs.append(f"Обычный цикл завершен за: {duration_seq:.4f} секунд.")
        start_mp = time.perf_counter()
        with ProcessPoolExecutor() as executor:
            _ = list(executor.map(Infrastructure.calculate_collision_vector, data, chunksize=500))
            
        duration_mp = time.perf_counter() - start_mp
        logs.append(f"Multiprocessing завершен за: {duration_mp:.4f} секунд.")
        speedup = duration_seq / duration_mp if duration_mp > 0 else 0
        logs.append(f"Ускорение: в {speedup:.2f} раз(а).")
        return {
            'logs': "\n".join(logs),
            'seq_time': round(duration_seq, 4),
            'parallel_time': round(duration_mp, 4)
        }

    @staticmethod
    async def fetch_texture_data(texture_id: int, logs: list):
        logs.append(f"Начата подгрузка текстуры {texture_id}.")
        wait_time = round(random.uniform(0.1, 0.5), 2)
        await asyncio.sleep(wait_time)
        logs.append(f"Подгрузка текстуры {texture_id} завершена за {wait_time} секунд.")

    @staticmethod
    def run_asyncio_test():
        logs = []

        async def main():
            tasks = [Infrastructure.fetch_texture_data(i, logs) for i in range(20)]
            await asyncio.gather(*tasks)

        start_time = time.perf_counter()
        asyncio.run(main())
        duration = time.perf_counter() - start_time
        logs.append(f"Все текстуры загружены конкурентно за: {duration:.4f} секунд.")
        return {
            'logs': "\n".join(logs),
            'time': round(duration, 4)
        }