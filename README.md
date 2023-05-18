# NmapMulti
scanning per asset with applicable port


if you have a list of subdomains with ports , such as:

x.y.com:21
x.y.com:22
x.y.com:443
a.y.com:8080
a.y.com:3389

this script does the following nmap scan:

nmap -p (applicable port) --script=vulners.nsw subdomina



