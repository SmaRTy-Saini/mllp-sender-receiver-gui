
# Simple MLLP Sender/Receiver GUI

A desktop GUI tool to send and receive HL7 messages using MLLP, developed by **SmaRTy Saini Corp**.

## Features

- Send HL7 messages via MLLP (with START_BLOCK/END_BLOCK)
- Receive HL7 messages and view logs
- Auto-sends ACK to sender
- Simple Python GUI (Tkinter)
- Offline use, perfect for HL7 interface testing

## How to Use

1. Run the script with Python 3
2. Use the top section to paste a message and send
3. Use the bottom section to listen for incoming messages
4. Test locally using `127.0.0.1` and port `2575`

You can convert this to an EXE using PyInstaller:

```
pyinstaller --onefile --noconsole mllp_tool.py
```
