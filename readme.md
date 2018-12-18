# Network Graph Statistics

These python tools rely on `ss` (from iproute2) to read all/most TCP socket statistics from the kernel.

## Usage

Run an application you want to monitor.

```./collect.py```

will collect the network statistics into `ss.txt`
(the ss.txt output can be merged simply with other ss.txt files (possibly collected from other machines at the same time) by stripping the first lines from all but one file and then appending the other files to the file with the header)

```./parse.py```

will parse the `ss` output into a python dictionary

```./graph.py```

will produce a network graph using the latency and bandwidth statistics
