import socket
import mss
from PIL import Image
import struct
import pygame
import io
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('HOST')
PORT = 23000
BUFFER_SIZE = 65535
FPS = 30