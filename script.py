import urllib.parse
import socket
import os

processed_links = []
counter = 1

if os.path.exists("raw_links.txt"):
    with open("raw_links.txt", "r") as f:
        lines = f.read().splitlines()

    for line in lines:
        line = line.strip()
        if not line.startswith("vless://"):
            continue
        
        try:
            if "security=reality" not in line.lower():
                continue
            
            has_valid_transport = False
            for t in ["type=grpc", "type=tcp", "type=http", "type=splithttp"]:
                if t in line.lower():
                    has_valid_transport = True
                    break
            if not has_valid_transport:
                continue

            parsed = urllib.parse.urlparse(line)
            host_with_port = parsed.netloc.split("@")[-1]
            
            if ":" in host_with_port:
                host, port_str = host_with_port.split(":")
                port = int(port_str)
            else:
                host = host_with_port
                port = 443

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.0)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result != 0:
                continue
                
            clean_vless_part = line.split("#")[0]
            
            new_name_text = f"🇪🇺 📶LTE | ТЕСТ #{counter}"
            new_name_encoded = urllib.parse.quote(new_name_text)
            
            processed_links.append(f"{clean_vless_part}#{new_name_encoded}")
            counter += 1
        except Exception:
            continue

with open("temp.txt", "a") as f:
    for link in processed_links:
        f.write(link + "\n")
