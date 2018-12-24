#!/usr/bin/env python3

import sys
import re
import pickle
from si_prefix import si_parse

info_line_re = re.compile(
    r"(?P<state>\S{1,1})\s*"
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
    r"(rwnd_limited:(?P<rwnd_limited>\S+)\s+|)"
    r"(sndbuf_limited:(?P<sndbuf_limited>\S+)\s+|)"
    r"(unacked:(?P<unacked>\S+)\s+|)"
    r"(retrans:(?P<retrans>\S+)\s+|)"
    r"(lost:(?P<lost>\S+)\s+|)"
    r"(rcv_rtt:(?P<rcv_rtt>\S+)\s+|)"
    r"rcv_space:(?P<rcv_space>\S+)\s+"
    r"rcv_ssthresh:(?P<rcv_ssthresh>\S+)\s+"
    r"(notsent:(?P<notsent>\S+)\s+|)"
    r"minrtt:(?P<minrtt>\S+)"
)

user_re = re.compile(
    r'"(?P<name>[^"]+)",pid=(?P<pid>\w+),fd=(?P<fd>\w+)'
)
def parse_users(users):
    ms = []
    for user in users[1:-1].split('),('):
        m = re.match(user_re, user)
        if not m:
            print('failed to parse user: {}'.format(user))
            sys.exit(1)
        ms.append(m.groupdict())
    return ms

def parse_rtt(rtt_str):
    s = rtt_str.split('/')
    return {'rtt_avg': float(s[0]), 'rtt_std_dev': float(s[1])}
def parse_bps(bps_str):
    assert(bps_str.endswith('bps'))
    bps_str = bps_str.replace('K', 'k')
    return si_parse(bps_str[:-3])
def parse_address(addr_str):
    host, port = addr_str.rsplit(':', 1)
    return {'host': host, 'port': port}

def main():
    file = open('ss.txt', 'r')
    lines = file.readlines()
    connections = []
    for info_line, details_line in zip(lines[0::2], lines[1::2]):
        info_m = re.match(info_line_re, info_line)
        if not info_m:
            print('failed to parse info line: {}'.format(info_line))
            sys.exit(1)
        info = info_m.groupdict()
        details_m = re.match(details_line_re, details_line)
        if not details_m:
            print('failed to parse details line: {}'.format(details_line))
            sys.exit(1)
        details = details_m.groupdict()
        users_str = info['users']
        users = None
        if users_str:
            users = parse_users(users_str)
        local_pid = None
        if not users:
            continue
        if len(users) > 0:
            local_pid = int(users[0]['pid'])
        peer_pid = None
        if len(users) > 1:
            peer_pid = int(users[1]['pid'])
        local_addr = parse_address(info['local_addr'])
        peer_addr = parse_address(info['peer_addr'])
        rtt_avg = parse_rtt(details['rtt'])['rtt_avg']
        rtt_sd = parse_rtt(details['rtt'])['rtt_std_dev']
        send_bandwidth = parse_bps(details['send'])
        #this merges the two dictionaries into one
        connection = {**info, **details}
        connection['rtt_avg'] = rtt_avg
        connection['rtt_sd'] = rtt_sd
        connection['send_bandwidth'] = send_bandwidth
        connection['local_pid'] = local_pid
        connection['peer_pid'] = peer_pid
        connection['local_addr_parsed'] = local_addr
        connection['peer_addr_parsed'] = peer_addr
        connection['users'] = users
        connections.append(connection)

    pickle.dump(connections, open('connections.pickle', 'wb'))

if __name__ == '__main__':
    main()
