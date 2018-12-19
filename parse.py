#!/usr/bin/env python3

import re
import pickle

file = open('ss.txt', 'r')

info_line_re = re.compile(
    r"(?P<recv_q>\S+)\s+"
    r"(?P<send_q>\S+)\s+"
    r"(?P<local_addr>\S+)\s+"
    r"(?P<peer_addr>\S+)\s+"
    r"(users:\((?P<users>\S+)\)|)\s+"
)

details_line_re = re.compile(
    r"\s+"
    r"cubic wscale:(?P<cubic_wscale>\S+)\s+"
    r"rto:(?P<rto>\S+)\s+"
    r"rtt:(?P<rtt>\S+)\s+"
    r"(ato:(?P<ato>\S+)\s+|)"
    r"mss:(?P<mss>\S+)\s+"
    r"pmtu:(?P<pmtu>\S+)\s+"
    r"rcvmss:(?P<rcvmss>\S+)\s+"
    r"advmss:(?P<advmss>\S+)\s+"
    r"cwnd:(?P<cwnd>\S+)\s+"
    r"(ssthresh:(?P<ssthresh>\S+)\s+|)"
    r"(bytes_acked:(?P<bytes_acked>\S+)\s+|)"
    r"(bytes_received:(?P<bytes_received>\S+)\s+|)"
    r"(segs_out:(?P<segs_out>\S+)\s+|)"
    r"(segs_in:(?P<segs_in>\S+)\s+|)"
    r"(data_segs_out:(?P<data_segs_out>\S+)\s+|)"
    r"(data_segs_in:(?P<data_segs_in>\S+)\s+|)"
    r"send (?P<send>\S+)\s+"
    r"(lastsnd:(?P<lastsnd>\S+)\s+|)"
    r"(lastrcv:(?P<lastrcv>\S+)\s+|)"
    r"(lastack:(?P<lastack>\S+)\s+|)"
    r"(pacing_rate (?P<pacing_rate>\S+)\s+|)"
    r"(delivery_rate (?P<delivery_rate>\S+)\s+|)"
    r"(?P<app_limited>app_limited\s+|)"
    r"(busy:(?P<busy>\S+)\s+|)"
    r"(sndbuf_limited:(?P<sndbuf_limited>\S+)\s+|)"
    r"(rwnd_limited:(?P<rwnd_limited>\S+)\s+|)"
    r"(retrans:(?P<retrans>\S+)\s+|)"
    r"(unacked:(?P<unacked>\S+)\s+|)"
    r"(rcv_rtt:(?P<rcv_rtt>\S+)\s+|)"
    r"rcv_space:(?P<rcv_space>\S+)\s+"
    r"rcv_ssthresh:(?P<rcv_ssthresh>\S+)\s+"
    r"(notsent:(?P<notsent>\S+)\s+|)"
    r"minrtt:(?P<minrtt>\S+)"
)

lines = file.readlines()
edges = []
for info_line, details_line in zip(lines[0::2], lines[1::2]):
    m = re.match(info_line_re, info_line)
    n = re.match(details_line_re, details_line)
    #this merges the two dictionaries into one
    edge = {**m.groupdict(), **n.groupdict()}
    edge['weight'] = 1
    edge_tuple = (edge['local_addr'], edge['peer_addr'], edge)
    edges.append(edge_tuple)

pickle.dump(edges, open('edges.pickle', 'wb'))
