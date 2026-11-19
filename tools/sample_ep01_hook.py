"""Sample 15 saat hook Episod 1, dijana sepenuhnya dengan code (tanpa AI).

Guna: python3 tools/sample_ep01_hook.py <output_dir>
Hasil: <output_dir>/sample_ep01.mp4 (1080x1920, 30fps)
"""
import math
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS, DUR = 1080, 1920, 30, 15.0
N = int(FPS * DUR)
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(13)

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_S = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

# Door geometry (vanishing frame at the end of the hallway)
DX0, DY0, DX1, DY1 = 400, 640, 680, 1240

KNOCKS = [5.0, 5.7, 6.4]


def lerp(a, b, t):
    return a + (b - a) * t


def smooth(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


# ---------- static layers ----------
def hallway():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(img)
    wall = (14, 28, 30)
    d.polygon([(0, 0), (DX0, DY0), (DX0, DY1), (0, H)], fill=wall)
    d.polygon([(W, 0), (DX1, DY0), (DX1, DY1), (W, H)], fill=(11, 23, 25))
    d.polygon([(0, 0), (W, 0), (DX1, DY0), (DX0, DY0)], fill=(6, 12, 14))
    d.polygon([(0, H), (W, H), (DX1, DY1), (DX0, DY1)], fill=(20, 16, 12))
    # floor planks converging
    for i in range(-6, 7):
        x_far = (DX0 + DX1) / 2 + i * 22
        x_near = W / 2 + i * 190
        d.line([(x_far, DY1), (x_near, H)], fill=(12, 9, 7), width=3)
    # wall trim lines
    for k in (0.25, 0.55):
        d.line([(0, lerp(0, H, k)), (DX0, lerp(DY0, DY1, k))], fill=(8, 16, 17), width=4)
        d.line([(W, lerp(0, H, k)), (DX1, lerp(DY0, DY1, k))], fill=(7, 14, 15), width=4)
    # door
    d.rectangle([DX0 - 18, DY0 - 18, DX1 + 18, DY1], fill=(26, 18, 12))
    d.rectangle([DX0, DY0, DX1, DY1 - 6], fill=(34, 22, 14))
    for y0, y1 in ((DY0 + 40, DY0 + 260), (DY0 + 320, DY1 - 50)):
        d.rectangle([DX0 + 35, y0, DX1 - 35, y1], outline=(22, 14, 9), width=6)
    d.ellipse([DX1 - 60, 940, DX1 - 36, 964], fill=(70, 58, 30))
    # padlock
    d.rectangle([DX1 - 66, 985, DX1 - 30, 1020], fill=(40, 40, 38))
    d.arc([DX1 - 62, 965, DX1 - 34, 995], 180, 360, fill=(40, 40, 38), width=5)
    return np.asarray(img, dtype=np.float32)


def glow_layer():
    g = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(g)
    d.rectangle([DX0 + 4, DY1 - 8, DX1 - 4, DY1 + 2], fill=255)
    g = g.filter(ImageFilter.GaussianBlur(26))
    a = np.asarray(g, dtype=np.float32)[..., None] / 255.0
    return a * np.array([255, 190, 90], dtype=np.float32) * 1.6


def vignette():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((x - W / 2) / (W * 0.62)) ** 2 + ((y - H * 0.5) / (H * 0.55)) ** 2)
    return np.clip(1.15 - r * 0.85, 0.12, 1.0)[..., None]


def clock_scene():
    img = Image.new("RGB", (W, H), (8, 15, 20))
    d = ImageDraw.Draw(img)
    cx, cy, R = W // 2, 860, 300
    d.ellipse([cx - R - 30, cy - R - 30, cx + R + 30, cy + R + 30], fill=(30, 20, 13))
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(118, 122, 118))
    for i in range(12):
        a = math.radians(i * 30)
        r0, r1 = R - 40, R - 12
        d.line([(cx + r0 * math.sin(a), cy - r0 * math.cos(a)),
                (cx + r1 * math.sin(a), cy - r1 * math.cos(a))], fill=(25, 25, 25), width=10)
    for ang, ln, wd in ((96.5, 0.5, 18), (78, 0.8, 10)):  # 3:13
        a = math.radians(ang)
        d.line([(cx, cy), (cx + R * ln * math.sin(a), cy - R * ln * math.cos(a))],
               fill=(15, 15, 15), width=wd)
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(15, 15, 15))
    d.line([(cx, cy + R + 30), (cx, cy + R + 330)], fill=(24, 16, 10), width=14)  # pendulum rod
    d.ellipse([cx - 55, cy + R + 300, cx + 55, cy + R + 410], fill=(60, 48, 24))
    arr = np.asarray(img, dtype=np.float32)
    # bluish moonlight wash from the left
    x = np.linspace(1.0, 0.35, W, dtype=np.float32)[None, :, None]
    return arr * x * np.array([0.85, 0.95, 1.15], dtype=np.float32)


BASE = hallway()
GLOW = glow_layer()
VIG = vignette()
CLOCK = clock_scene()
GRAIN = [rng.normal(0, 9, (H // 2, W // 2, 1)).astype(np.float32) for _ in range(8)]


def font(path, size):
    return ImageFont.truetype(path, size)


F_HOOK = font(FONT_B, 66)
F_SUB = font(FONT_B, 50)
F_BIG = font(FONT_B, 120)
F_NOTE = font(FONT_S, 64)
F_END = font(FONT_B, 58)


def wrap(text, f, maxw, d):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    lines.append(cur)
    return lines


def draw_text(img, text, f, y, alpha=1.0, fill=(255, 255, 255), stroke=6, box=None):
    if alpha <= 0:
        return
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    lines = wrap(text, f, W - 140, d)
    lh = f.size + 18
    if box:
        top = y - 24
        bot = y + lh * len(lines) + 10
        d.rounded_rectangle([50, top, W - 50, bot], 24, fill=box)
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=f)
        d.text(((W - tw) / 2, y + i * lh), ln, font=f, fill=fill + (255,),
               stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    if alpha < 1:
        a = layer.getchannel("A").point(lambda v: int(v * alpha))
        layer.putalpha(a)
    img.alpha_composite(layer)


def zoom(arr, z, ox=0.0, oy=0.0, cy=0.5):
    if z <= 1.0001 and ox == 0 and oy == 0:
        return arr
    cw, ch = W / z, H / z
    x0 = (W - cw) / 2 + ox
    y0 = (H - ch) * cy + oy
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    return np.asarray(img.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch)),
                      dtype=np.float32)


def knock_env(t):
    return sum(math.exp(-(t - k) * 9) for k in KNOCKS if t >= k)


def paper_layer(p):
    """Paper sliding out from under the door, p in [0,1]."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    y = lerp(DY1 - 4, DY1 + 150, p)
    s = lerp(0.45, 1.0, p)
    cx = (DX0 + DX1) / 2 + 10
    hw, hh = 150 * s, 55 * s
    d.polygon([(cx - hw, y), (cx + hw, y - 6 * s), (cx + hw * 1.15, y + hh), (cx - hw * 1.1, y + hh + 4)],
              fill=(196, 178, 128, 255))
    d.line([(cx - hw * 0.2, y + 3), (cx - hw * 0.1, y + hh)], fill=(160, 140, 95, 255), width=3)
    return img


def scene_frame(t):
    # --- Scene A: hallway (0-8s) ---
    if t < 8.0:
        z = lerp(1.0, 1.55, smooth(t / 8.0))
        flick = 0.55 + 0.25 * math.sin(t * 7.3) * math.sin(t * 2.1)
        k = knock_env(t)
        flick += 0.9 * k
        arr = BASE + GLOW * flick
        sh = 22 * k
        arr = zoom(arr, z, ox=rng.uniform(-sh, sh), oy=rng.uniform(-sh, sh), cy=0.52)
        fade = smooth(t / 0.6) * (1 - smooth((t - 7.75) / 0.25))
        return arr * fade, None
    # --- Scene B: clock (8-10.5s) ---
    if t < 10.5:
        lt = t - 8.0
        arr = zoom(CLOCK, lerp(1.0, 1.18, lt / 2.5), cy=0.45)
        fade = smooth(lt / 0.3) * (1 - smooth((lt - 2.25) / 0.25))
        return arr * fade, None
    # --- Scene C: back to door, dark, then paper (10.5-15s) ---
    lt = t - 10.5
    flick = 0.25 if lt < 1.0 else 0.45 + 0.1 * math.sin(t * 9)
    arr = zoom(BASE + GLOW * flick, 1.75, cy=0.58)
    fade = smooth(lt / 0.4)
    paper = None
    if lt >= 1.0:
        p = smooth((lt - 1.0) / 2.0)
        paper = paper_layer(p)
    return arr * fade, paper


SUBS = [
    (0.5, 4.4, "Korang pernah dengar orang ketuk pintu... dari dalam bilik yang berkunci?"),
    (4.9, 7.9, "tok... tok... tok..."),
    (8.3, 10.4, "Jam tunjuk... tiga tiga belas pagi."),
    (11.6, 13.4, "Lepas tu... ada benda keluar bawah pintu."),
]


def render_frame(i):
    t = i / FPS
    arr, paper = scene_frame(t)
    arr = arr * VIG
    g = GRAIN[i % len(GRAIN)]
    arr = arr + np.repeat(np.repeat(g, 2, 0), 2, 1)
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    if paper is not None:
        # paper is drawn in the zoomed (1.75x) space: map door coords by same zoom
        z, cy = 1.75, 0.58
        cw, ch = W / z, H / z
        x0, y0 = (W - cw) / 2, (H - ch) * cy
        pz = paper.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))
        img.alpha_composite(pz)

    # hook text (top)
    if t < 8.0:
        a = smooth((t - 0.3) / 0.7)
        draw_text(img, "Ketukan dari DALAM bilik berkunci", F_HOOK, 230, a,
                  fill=(255, 255, 255), box=(150, 10, 10, int(200 * a)))
    if 8.2 < t < 10.4:
        draw_text(img, "3:13 AM", F_BIG, 1420, smooth((t - 8.2) / 0.4), fill=(230, 60, 60))

    # closing note + end card
    if t >= 13.5:
        a = smooth((t - 13.5) / 0.5)
        dark = Image.new("RGBA", img.size, (0, 0, 0, int(170 * a)))
        img.alpha_composite(dark)
        note = Image.new("RGBA", img.size, (0, 0, 0, 0))
        nd = ImageDraw.Draw(note)
        nd.rectangle([110, 640, W - 110, 1180], fill=(205, 188, 140, int(255 * a)))
        img.alpha_composite(note)
        draw_text(img, "Selamat datang.", F_NOTE, 760, a, fill=(60, 20, 15), stroke=0)
        draw_text(img, "Kali ni jangan lari.", F_NOTE, 900, a, fill=(120, 15, 15), stroke=0)
        draw_text(img, "Part 2 esok malam 8:30", F_END, 1500, smooth((t - 14.0) / 0.4))

    # subtitles
    for s0, s1, txt in SUBS:
        if s0 <= t <= s1:
            a = min(smooth((t - s0) / 0.2), smooth((s1 - t) / 0.2))
            draw_text(img, txt, F_SUB, 1640, a)
    return img.convert("RGB").tobytes()


# ---------- audio ----------
SR = 44100


def audio():
    n = int(SR * DUR)
    t = np.arange(n) / SR
    drone = 0.10 * np.sin(2 * np.pi * 55 * t) + 0.06 * np.sin(2 * np.pi * 82.5 * t + 1.3)
    drone *= 0.7 + 0.3 * np.sin(2 * np.pi * 0.11 * t)
    noise = rng.normal(0, 1, n)
    rumble = np.convolve(noise, np.ones(400) / 400, mode="same") * 0.6
    bed = drone + rumble
    # silence before the paper (10.5-11.5s)
    env = np.ones(n)
    s0, s1 = int(10.4 * SR), int(11.6 * SR)
    env[s0:s1] = 0.05
    bed *= env
    out = bed.copy()

    def add(sig, at, gain=1.0):
        i = int(at * SR)
        j = min(n, i + len(sig))
        out[i:j] += sig[: j - i] * gain

    kt = np.arange(int(0.35 * SR)) / SR
    knock = (np.sin(2 * np.pi * 95 * kt) * np.exp(-kt * 22)
             + rng.normal(0, 1, len(kt)) * np.exp(-kt * 60) * 0.5)
    for k in KNOCKS:
        add(knock, k, 0.9)
    tt = np.arange(int(0.05 * SR)) / SR
    tick = rng.normal(0, 1, len(tt)) * np.exp(-tt * 120)
    for s in np.arange(8.4, 10.4, 1.0):
        add(tick, s, 0.35)
    slide_len = int(1.8 * SR)
    sl = np.convolve(rng.normal(0, 1, slide_len), np.ones(30) / 30, mode="same")
    sl *= np.sin(np.linspace(0, np.pi, slide_len)) * 0.5
    add(sl, 11.6)
    bt = np.arange(int(1.5 * SR)) / SR
    boom = np.sin(2 * np.pi * 45 * bt) * np.exp(-bt * 2.5)
    add(boom, 13.5, 0.8)
    out = np.clip(out / max(1e-6, np.abs(out).max()) * 0.85, -1, 1)
    pcm = (out * 32767).astype(np.int16)
    path = OUT / "sample_audio.wav"
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(pcm.tobytes())
    return path


def main():
    wav = audio()
    mp4 = OUT / "sample_ep01.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", str(wav), "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest", str(mp4)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(N):
        p.stdin.write(render_frame(i))
    p.stdin.close()
    p.wait()
    print(mp4)


if __name__ == "__main__":
    main()
