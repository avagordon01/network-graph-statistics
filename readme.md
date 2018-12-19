# Network Graph Statistics

These python tools rely on `ss` (from iproute2) to read all/most TCP socket statistics from the kernel.

## Usage

Run an application you want to monitor. Then

```./collect.sh HOSTS```

will collect the network statistics from `HOSTS`

```./parse.py```

will parse the `ss` output into a python dictionary

```./graph.py```

will produce a network graph using the latency and bandwidth statistics
