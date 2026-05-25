from settings import *
import protocol

class Client:
    def __init__(self, socket: socket.socket, run_program: bool):
        self.run_program = run_program

        self.socket = socket
        self.frame_id = 0
        self.img_size = None

    def take_screenshot(self):
        while self.run_program:
            with mss.mss() as sct:
                monitor = sct.monitors[1]
                img = sct.grab(monitor)
                self.img_size = img.size
                pil_img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
                byte_io = io.BytesIO()
                pil_img.save(byte_io, format = "JPEG", quality = 70)
                jpeg_bytes = byte_io.getvalue()

                protocol.send_screenshot(
                    jpeg_bytes,
                    self.socket,
                    self.frame_id,
                    HOST
                )

                #Each frame contains a lot of chunks
                self.frame_id += 1

if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_obj = Client(client_socket, True)
    client_obj.take_screenshot()
