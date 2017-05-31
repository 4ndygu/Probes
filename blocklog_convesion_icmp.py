import sys

def read_subplot_data(filename):
    data_f = open(filename, "r")
    res = []
    for line in data_f:
        line = line.rstrip()
        if line.startswith('#fsdb'):
            expected_schema = '#fsdb -F t reply_type	time_s	rtt_us	ttl	probe_addr	reply_addr'
            if line != expected_schema:
                raise ValueError('input file format has odd schema: ' + line + "\n\tnot " + expected_schema)
        if line.startswith('#'):
            continue
        if line == "":
            break
        f = line.strip().split('\t')
        if str(f[4]) == "        --------":
            continue

        reply_type = str(f[0])
        time = str(f[1])
        probe_addr = str(f[4])

        if reply_type[3] == '8' or reply_type[3] == '5':
            reply_type = '2'
        elif reply_type[3] == '0':
            reply_type = '1'
        else:
            reply_type = '3'

        a = probe_addr.split('.')
        probe_addr = ""
        for item in a:
            if len(hex(int(item))[2:]) == 1:
                probe_addr = probe_addr + '0' + hex(int(item))[2:]
            else:
                probe_addr = probe_addr + hex(int(item))[2:]

        seq = (time, probe_addr, reply_type)
        print "\t".join(seq)
        del res[:]

read_subplot_data(sys.argv[1]) 
