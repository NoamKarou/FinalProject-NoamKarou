import multiprocessing

class MyClass:
    def __init__(self):
        self.num_cores = multiprocessing.cpu_count()

    def mining_thread(self):
        print("Processing")

    def run(self, funtion):
        pool = multiprocessing.Pool(processes=self.num_cores)
        for _ in range(self.num_cores):  # Launch one process per core
            pool.apply_async(funtion)
        pool.close()
        pool.join()

if __name__ == '__main__':
    my_instance = MyClass()
    my_instance.run(my_instance.mining_thread)
