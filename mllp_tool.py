
import tkinter as tk
from tkinter import scrolledtext, messagebox
import socket
import threading

START_BLOCK = b'\x0b'
END_BLOCK = b'\x1c'
CARRIAGE_RETURN = b'\x0d'

class MLLPTool:
    def __init__(self, master):
        self.master = master
        master.title("MLLP Sender/Receiver - SmaRTy Saini Corp")

        # Sender
        tk.Label(master, text="MLLP Sender").grid(row=0, column=0, sticky="w", padx=10)
        self.sender_text = scrolledtext.ScrolledText(master, width=60, height=10)
        self.sender_text.grid(row=1, column=0, padx=10)
        self.ip_entry = tk.Entry(master)
        self.port_entry = tk.Entry(master)
        self.ip_entry.insert(0, "127.0.0.1")
        self.port_entry.insert(0, "2575")
        tk.Label(master, text="IP:").grid(row=2, column=0, sticky="w", padx=10)
        self.ip_entry.grid(row=2, column=0, sticky="e", padx=70)
        tk.Label(master, text="Port:").grid(row=2, column=0, sticky="e", padx=160)
        self.port_entry.grid(row=2, column=0, sticky="e", padx=210)
        tk.Button(master, text="Send via MLLP", command=self.send_message).grid(row=3, column=0, pady=5)

        # Separator
        tk.Label(master, text="-"*120).grid(row=4, column=0)

        # Receiver
        tk.Label(master, text="MLLP Receiver (Listener)").grid(row=5, column=0, sticky="w", padx=10)
        self.recv_port_entry = tk.Entry(master)
        self.recv_port_entry.insert(0, "2575")
        self.recv_log = scrolledtext.ScrolledText(master, width=60, height=10)
        self.recv_log.grid(row=6, column=0, padx=10)
        tk.Label(master, text="Listen Port:").grid(row=7, column=0, sticky="w", padx=10)
        self.recv_port_entry.grid(row=7, column=0, sticky="e", padx=80)
        tk.Button(master, text="Start Receiver", command=self.start_server).grid(row=8, column=0, pady=5)

    def send_message(self):
        ip = self.ip_entry.get()
        port = int(self.port_entry.get())
        msg = self.sender_text.get("1.0", tk.END).strip().encode()
        hl7_msg = START_BLOCK + msg + END_BLOCK + CARRIAGE_RETURN
        try:
            with socket.create_connection((ip, port), timeout=10) as sock:
                sock.sendall(hl7_msg)
                ack = sock.recv(4096)
                messagebox.showinfo("Success", f"Message sent!\nACK: {ack.decode(errors='ignore')}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def start_server(self):
        port = int(self.recv_port_entry.get())
        threading.Thread(target=self.run_server, args=(port,), daemon=True).start()
        messagebox.showinfo("Receiver", f"Listening on port {port}")

    def run_server(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind(("0.0.0.0", port))
            server.listen()
            while True:
                client, addr = server.accept()
                with client:
                    data = b""
                    while True:
                        chunk = client.recv(1024)
                        if not chunk:
                            break
                        data += chunk
                        if END_BLOCK in chunk:
                            break
                    # Clean message
                    msg = data.replace(START_BLOCK, b"").replace(END_BLOCK, b"").replace(CARRIAGE_RETURN, b"")
                    decoded = msg.decode(errors='ignore')
                    self.recv_log.insert(tk.END, f"Received from {addr}:\n{decoded}\n\n")
                    self.recv_log.see(tk.END)
                    # Send ACK
                    ack_msg = START_BLOCK + b"MSH|^~\\&|ACK|SERVER|CLIENT|ACK|202504121230||ACK^A01|1|P|2.3" + END_BLOCK + CARRIAGE_RETURN
                    client.sendall(ack_msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = MLLPTool(root)
    root.mainloop()
