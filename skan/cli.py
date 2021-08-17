#!/usr/local/bin/python3
""" main app for a multi-threaded network port scanner """
#########
#  skan.py
#
#  Description:
#  multi-threaded network port scanner
#
#  Author:
#  Stephen Eaton <seaton@strobotics.com.au>

import argparse
import socket
import ipaddress
import threading
from queue import Queue

VERSION = "0.0.1"

# get and parse command line arguments
PARSER = argparse.ArgumentParser(
    description="Perform a network port scan \
                    of a host IP address"
)
PARSER.add_argument(
    "target", type=str, metavar="target_ip", help="Target IP address (xxx.xxx.xxx.xxx)"
)
PARSER.add_argument(
    "-s",
    "--startport",
    type=int,
    metavar="",
    default=1,
    help="Port number to start scanning (default: 1)",
    required=False,
)
PARSER.add_argument(
    "-e",
    "--endport",
    type=int,
    metavar="",
    default=1024,
    help="End port number of scan range (default: 1024,  max: 65535)",
    required=False,
)
PARSER.add_argument(
    "-t",
    "--threads",
    type=int,
    metavar="",
    default=32,
    help="number of scan threads to run (default: 32, max: 1024)",
    required=False,
)
PARSER.add_argument(
    "--version",
    action="version",
    version="%(prog)s v" + VERSION,
    help="prints version information",
)
ARGS = PARSER.parse_args()

# queue for all the ports to scan
SCAN_QUEUE = Queue()

# define a resource lock i.e. only one thread can print to stdio at a time
#   so thread needs to lock the resource while printing
MUTEX_PRINT = threading.Lock()


def validate_args():
    "arguments bounds checking and validation"

    # valide the IP address and exit with an error
    try:
        ipaddress.IPv4Address(ARGS.target)
    except ValueError:
        print("ERROR - IP address is invalid: %s" % ARGS.target)
        exit(1)

    if ARGS.startport <= 0:
        ARGS.startport = 1

    ARGS.endport = min(ARGS.endport, 65535)

    # check that start and end are correct
    ARGS.startport = min(ARGS.startport, ARGS.endport)
    # dont create unused threads if we can help it
    ARGS.threads = min(ARGS.threads, ARGS.endport - ARGS.startport)
    ARGS.threads = max(ARGS.threads, 1)
    ARGS.threads = min(ARGS.threads, 1024)


def scan_port(port):
    "scan_port will attempt to connect to the target IP on the given port"
    "if the connection is successful then prints the open port number"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn = sock.connect((ARGS.target, port))

        # acquire lock and print to stdio
        with MUTEX_PRINT:
            print("port", port, ":open")

        conn.close()
    except:
        pass


def get_scan_job():
    "get the next port to scan from the queue"
    while True:
        # gets next port to scan from queue
        port = SCAN_QUEUE.get()
        scan_port(port)
        # signal queue that job has been completed
        SCAN_QUEUE.task_done()


def start_worker_threads(count):
    "starts the requested amount of worker threads"
    for x in range(count + 1):
        w = threading.Thread(target=get_scan_job)
        w.daemon = True
        w.start()


def queue_ports():
    "queues the ports for scanning, each thread will de-queue a port to scan until queue is empty"
    for port in range(ARGS.startport, ARGS.endport + 1):
        SCAN_QUEUE.put(port)


def main():
    """Main application"""

    validate_args()

    print("")
    print(PARSER.prog, "v", VERSION)
    print(
        "Scanning IP:",
        ARGS.target,
        "ports:",
        ARGS.startport,
        "-",
        ARGS.endport,
        "threads:",
        ARGS.threads,
    )
    print("-=================================================================-")
    # setup ports to scan and start worker threads
    queue_ports()
    start_worker_threads(ARGS.threads)

    # wait for all scans to complete before exiting app
    SCAN_QUEUE.join()


if __name__ == "__main__":
    main()
