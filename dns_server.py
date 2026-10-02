import socket
import dns.message
import dns.rdatatype
import base64

chunks= {}


HOST = "127.0.0.1"
port = 5999

sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
sock.bind ((HOST ,port))


print(f"DNS server listening on {HOST}:{port}")


total_chunks=0

while True:
    data,addr = sock.recvfrom(4096)

    request = dns.message.from_wire(data)

    question = request.question[0]

    qname = question.name.to_text()

    qtype = dns.rdatatype.to_text(question.rdtype)

    labels= qname.split(".")

    
    total_chunks=int(labels[0])

    sequence_number = int(labels[1])


    chunk = labels[2]

    chunks[sequence_number]=chunk

    print(f"\nReceived DNS query from {addr}")
    
    print(f"QNAME : {qname}")
    
    print(f"QTYPE : {qtype}")

    print(f"seq_no :{sequence_number}")
    print(f"chunk :{chunk}")
    print("=============================\n")


    


    response = dns.message.make_response(request)
    sock.sendto(response.to_wire(),addr)

   
    if sequence_number == total_chunks:
        print(f"total no of chunks are : {total_chunks}")
        break


received_encoded_data =""


for seq_no in sorted(chunks) :
    # print(f"{chunks[seq_no]} \n")
    received_encoded_data+=chunks[seq_no]

padding = "=" * ((8- len(received_encoded_data))%8) 


received_encoded_data += padding

decoded = base64.b32decode(received_encoded_data).decode("ascii")

print("========================\n")


print(decoded)





   
