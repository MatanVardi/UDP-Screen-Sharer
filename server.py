import socket
import io
import pygame
import protocol
from settings import HOST, PORT, FPS


class Server:
    def __init__(self, sock):
        self.sock = sock
        self.clock = pygame.time.Clock()

    def run_pygame(self):
        pygame.init()
        screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Screen Share - Server")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            try:
                jpeg_bytes = protocol.receive_data(self.sock)

                img = pygame.image.load(io.BytesIO(jpeg_bytes), "frame.jpg")
                if img.get_size() != screen.get_size():
                    screen = pygame.display.set_mode(img.get_size())
                    print(f"Window resized to {img.get_size()}")

                screen.blit(img, (0, 0))
                pygame.display.flip()
                self.clock.tick(FPS)

            except Exception as e:
                print("Error:", e)


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))
    print(f"Server listening on {HOST}:{PORT}")

    server = Server(server_socket)
    server.run_pygame()