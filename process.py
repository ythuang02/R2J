import multiprocessing

def build_worker_pool(Worker, tasks, results, args, indexes):
    workers = []

    for index in indexes:
        worker = multiprocessing.Process(target = Worker, args = (tasks, results, args, index, ))
        worker.start()
        workers.append(worker)

    return workers

def run_multiprocess(Saver, Saver_args, Worker, Worker_args, Worker_indexes, Loader, Loader_args):
    tasks = multiprocessing.Queue()
    results = multiprocessing.Queue()

    saver = multiprocessing.Process(target = Saver, args = (results, Saver_args,))
    saver.start()

    workers = build_worker_pool(Worker, tasks, results, Worker_args, Worker_indexes)
    Loader(tasks, Loader_args)

    for worker in workers:
        tasks.put(-1)
    for worker in workers:
        worker.join()
    
    results.put(-1)
    saver.join()