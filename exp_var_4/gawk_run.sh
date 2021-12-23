#!/bin/bash

gawk -i inplace '$3 ~ /5001$/' "tcp_probe_reno_h1_h2.txt"
gawk -i inplace '$3 ~ /5001$/' "tcp_probe_cubic_h1_h2.txt"

gawk -i inplace '$3 ~ /5001$/' "tcp_probe_reno_h2_h3.txt"
gawk -i inplace '$3 ~ /5001$/' "tcp_probe_cubic_h2_h3.txt"

gawk -i inplace '$3 ~ /5001$/' "tcp_probe_reno_h1_h3.txt"
gawk -i inplace '$3 ~ /5001$/' "tcp_probe_cubic_h1_h3.txt"