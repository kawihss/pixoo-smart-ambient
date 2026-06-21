from math import ceil
from PIL import Image
from pixoo import Pixoo


def _pixoo_send_image(p: Pixoo, img: Image.Image):
    nb_colors, palette, pixels = p.encode_raw_image(img)
    frame_size = 7 + len(pixels) + len(palette)
    frame = [0xAA, frame_size & 0xff, (frame_size >> 8) & 0xff,
             0, 0, 0, nb_colors] + palette + pixels
    total = len(frame)
    for i in range(ceil(total / 200)):
        chunk = [total & 0xff, (total >> 8) & 0xff, i]
        p.send(0x49, chunk + frame[i*200:(i+1)*200])


def push_to_pixoo(mac: str, img: Image.Image):
    p = Pixoo(mac)
    try:
        p.connect()
        p.set_box_mode(3)
        _pixoo_send_image(p, img)
    except OSError as e:
        print(f"[pixoo] connection failed: {e}")
    finally:
        if p.btsock:
            p.btsock.close()


def push_solid_color(mac: str, r: int, g: int, b: int):
    img = Image.new("RGB", (16, 16), (r, g, b))
    push_to_pixoo(mac, img)
