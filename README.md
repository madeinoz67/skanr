# skan

Multithreaded network port scanner for IPV4 addresses

## requirements

1. known Target host IP Address

## installation

`pip install skan`

## usage

### Help

Display the help

```
skan -h
usage: skan [-h] [-s] [-e] [-t] [--version] target_ip

Perform a network port scan of a host IP address

positional arguments:
  target_ip          Target IP address (xxx.xxx.xxx.xxx)

optional arguments:
  -h, --help         show this help message and exit
  -s , --startport   Port number to start scanning (default: 1)
  -e , --endport     End port number of scan range (default: 1024, max: 65535)
  -t , --threads     number of scan threads to run (default: 32, max: 1024)
  --version          prints version information
```

### basic IP scan

will scan an IP address from ports 1-1024 using 32 threads

```
skan 10.37.129.9

skan v 0.0.1
Scanning IP: 10.37.129.9 ports: 1 - 1024 threads: 32
-=================================================================-
port 21 :open
port 23 :open
port 22 :open
port 53 :open
port 80 :open
port 110 :open
port 111 :open
port 139 :open
port 143 :open
port 445 :open
port 901 :open
```

### scan port range on target

To scan a port range on the target machine use `-s` and `-e` to specify the start and end ports

if no start ot end prot is given then defaults apply

```
skan 10.37.129.9 -s 20 -e 100

skan.py v 0.0.1
Scanning IP: 10.37.129.9 ports: 20 - 100 threads: 32
-=================================================================-
port 21 :open
port 22 :open
port 23 :open
port 53 :open
port 80 :open
```

### specifing threads

To speed up the port scanning the number of threads can be passed using the `-t` argument up to a max of 1024 threads, to prevent starting unwanted threads, the number of threads started will never be greater than the number of ports to be scanned. 

```
skan 10.37.129.9 -e 65535 -t 1024

skan v 0.0.1
Scanning IP: 10.37.129.9 ports: 1 - 65535 threads: 1024
-=================================================================-
port 21 :open
port 22 :open
port 23 :open
port 53 :open
port 80 :open
port 110 :open
port 111 :open
port 139 :open
port 143 :open
port 445 :open
port 901 :open
port 2049 :open
port 6665 :open
port 6666 :open
port 6669 :open
port 6667 :open
port 6668 :open
port 8787 :open
port 37159 :open
port 44180 :open
port 50166 :open
```
