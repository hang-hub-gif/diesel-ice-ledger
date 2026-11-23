"""產生主畫面圖示（藍色底＋白色冰塊），不需要額外套件。

用法：python make_icons.py  → docs/icon-192.png、docs/icon-512.png、docs/apple-touch-icon.png
"""
import struct
import zlib
from pathlib import Path

DOCS = Path(__file__).resolve().parent / "docs"

TOP = (10, 108, 255)      # 背景上方顏色
BOTTOM = (0, 170, 220)    # 背景下方顏色
FACE_TOP = (255, 255, 255)
FACE_LEFT = (214, 236, 255)
FACE_RIGHT = (168, 210, 250)


def cube_faces():
    cx, cy, s = 0.5, 0.52, 0.25  # 冰塊放在中間 50%，Android 遮罩裁切也安全
    h = s * 0.866
    top, ur, lr = (cx, cy - s), (cx + h, cy - s / 2), (cx + h, cy + s / 2)
    bottom, ll, ul = (cx, cy + s), (cx - h, cy + s / 2), (cx - h, cy - s / 2)
    c = (cx, cy)
    return [
        ([top, ur, c, ul], FACE_TOP),
        ([ul, c, bottom, ll], FACE_LEFT),
        ([c, ur, lr, bottom], FACE_RIGHT),
    ]


def inside(poly, x, y):
    sign = 0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        cross = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)
        if cross != 0:
            if sign == 0:
                sign = 1 if cross > 0 else -1
            elif (cross > 0) != (sign > 0):
                return False
    return True


def color_at(x, y, faces):
    for poly, col in faces:
        if inside(poly, x, y):
            return col
    return tuple(round(TOP[i] + (BOTTOM[i] - TOP[i]) * y) for i in range(3))


def render(size):
    faces = cube_faces()
    sub = (0.25, 0.75)  # 2x2 取樣讓邊緣平滑
    rows = []
    for py in range(size):
        row = bytearray([0])
        for px in range(size):
            acc = [0, 0, 0]
            for sy in sub:
                for sx in sub:
                    c = color_at((px + sx) / size, (py + sy) / size, faces)
                    for i in range(3):
                        acc[i] += c[i]
            row += bytes(round(v / 4) for v in acc)
        rows.append(bytes(row))
    raw = b"".join(rows)

    def chunk(tag, data):
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")


def main():
    DOCS.mkdir(exist_ok=True)
    for name, size in (("icon-192.png", 192), ("icon-512.png", 512), ("apple-touch-icon.png", 180)):
        (DOCS / name).write_bytes(render(size))
        print("已輸出", name)


if __name__ == "__main__":
    main()
