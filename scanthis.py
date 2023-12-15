import subprocess
import threading
from queue import Queue

def worker(q):
    while True:
        subdomain, port = q.get()
        if subdomain is None:
            break

        print(f'Scanning {subdomain} on port {port}...')
        with open(f'{subdomain}_output.txt', 'w') as outfile:
            subprocess.run(['nmap', '-sV', '-p', str(port), '--script', 'vulners', subdomain], stdout=outfile)
        q.task_done()

def main():
    num_worker_threads = 10   # Change this number based on your needs
    subdomains_and_ports = Queue()

    # Start worker threads
    threads = []
    for i in range(num_worker_threads):
        t = threading.Thread(target=worker, args=(subdomains_and_ports,))
        t.start()
        threads.append(t)

    # Read subdomains and ports from file and add to queue
    with open('subdomains_and_ports.txt', 'r') as file:
        for line in file:
            subdomain, port = line.strip().split(':')
            subdomains_and_ports.put((subdomain, port))

    # Block until all tasks are done
    subdomains_and_ports.join()

    # Stop worker threads
    for i in range(num_worker_threads):
        subdomains_and_ports.put((None, None))
    for t in threads:
        t.join()

if __name__ == '__main__':
    main()
