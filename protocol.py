import struct
from settings import BUFFER_SIZE, PORT


MAX_PAYLOAD = 60000
HEADER_SIZE = 12


def send_screenshot(jpeg_bytes, sock, frame_id, addr):
    total_chunks = (len(jpeg_bytes) + MAX_PAYLOAD - 1) // MAX_PAYLOAD

    for chunk_id in range(total_chunks):
        start = chunk_id * MAX_PAYLOAD
        end = start + MAX_PAYLOAD
        chunk = jpeg_bytes[start:end]

        header = struct.pack("!III", frame_id, chunk_id, total_chunks)
        try:
            sock.sendto(header + chunk, (addr, PORT))
        except ConnectionResetError as e:
            print("Send error:", e)


def receive_data(sock):
    chunks = {}
    current_frame_id = None

    while True:
        packet, address = sock.recvfrom(BUFFER_SIZE)

        header = packet[:HEADER_SIZE]
        data = packet[HEADER_SIZE:]

        frame_id, chunk_id, total_chunks = struct.unpack("!III", header)

        if current_frame_id is not None and frame_id != current_frame_id:
            chunks = {}

        current_frame_id = frame_id
        chunks[chunk_id] = data

        if len(chunks) == total_chunks:
            full_frame = b"".join(chunks[i] for i in range(total_chunks))
            return full_frame