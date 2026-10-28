"""
build_cinematic_reel.py
Build a 9:16 Instagram Reel with cinematic festive visuals, floating golden bokeh,
smooth app viewport pan, subtitles, and neural voiceover narration.
"""
import asyncio
import http.server
import math
import os
import random
import socketserver
import subprocess
import threading
import cv2
import edge_tts
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

ASSETS_DIR = "cinematic_assets"
FINAL_VIDEO = "utsav_ai_cinematic_reel.mp4"
TEMP_VIDEO = "temp_render.mp4"
MASTER_AUDIO = "master_voiceover.wav"
WIDTH, HEIGHT = 720, 1280
FPS = 30

SCENES_DATA = [
    {
        "id": "intro",
        "tab": "ideas",
        "badge": "UTSAV AI • CELEBRATION COPILOT",
        "subtitle": "Planning an Indian wedding? Meet Utsav AI, built for Google Cloud Hackathon.",
        "tts": "Planning an Indian wedding or celebration? Meet Utsav AI, the intelligent celebration planner built for the Google Cloud Hackathon.",
    },
    {
        "id": "blueprint",
        "tab": "ideas",
        "badge": "STEP 1 • CULTURAL BLUEPRINTS",
        "subtitle": "Instant culturally-aware blueprints for Sangeet, Haldi & Muhurtham.",
        "tts": "In seconds, it designs culturally-aware blueprints for Sangeet, Haldi, and Muhurtham, complete with decor and ritual sequencing.",
    },
    {
        "id": "budget",
        "tab": "budget",
        "badge": "STEP 2 • BUDGET MAESTRO",
        "subtitle": "Real-time INR (₹) expense tracking with automated variance calculations.",
        "tts": "Budget Maestro automatically allocates your expenses in rupees, tracking caterers and decor with real-time variance calculations.",
    },
    {
        "id": "timeline",
        "tab": "timeline",
        "badge": "STEP 3 • RUN OF SHOW",
        "subtitle": "Minute-by-minute day-of schedule from Baraat entry to the Vidai.",
        "tts": "The Day-of Run of Show keeps your celebration synchronized minute by minute, from Baraat entry to the final Vidai.",
    },
    {
        "id": "genie",
        "tab": "chat",
        "badge": "STEP 4 • EVENTGENIE AI",
        "subtitle": "24/7 AI copilot powered by Gemini 2.5 for vendor quotes & negotiations.",
        "tts": "And EventGenie, powered by Google Gemini, acts as your twenty-four-seven copilot to negotiate vendor quotes and answer any query.",
    },
    {
        "id": "outro",
        "tab": "export",
        "badge": "BUILT WITH GEMINI & FASTAPI",
        "subtitle": "Live now on Render • Open source on GitHub! Try it today.",
        "tts": "Built with FastAPI and Google Gemini. Experience Utsav AI live on Render and open source on GitHub!",
    },
]

def get_font(size: int, bold: bool = False):
    font_names = [
        "C:/Windows/Fonts/segoeui.ttf" if not bold else "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arial.ttf" if not bold else "C:/Windows/Fonts/arialbd.ttf",
    ]
    for fn in font_names:
        if os.path.exists(fn):
            try:
                return ImageFont.truetype(fn, size)
            except Exception:
                pass
    return ImageFont.load_default()

async def generate_voiceovers():
    os.makedirs(ASSETS_DIR, exist_ok=True)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    durations = []
    
    print("Generating neural voiceover audio clips...")
    for idx, sc in enumerate(SCENES_DATA):
        audio_file = os.path.join(ASSETS_DIR, f"scene_{idx}.mp3")
        comm = edge_tts.Communicate(sc["tts"], "en-IN-NeerjaNeural", rate="+8%")
        await comm.save(audio_file)
        
        # Measure duration with ffmpeg
        res = subprocess.run([ffmpeg, "-i", audio_file], capture_output=True, text=True)
        dur = 5.0
        for line in res.stderr.splitlines():
            if "Duration:" in line:
                d_str = line.split("Duration:")[1].split(",")[0].strip()
                h, m, s = d_str.split(":")
                dur = float(h)*3600 + float(m)*60 + float(s)
                break
        sc["duration"] = dur + 0.3 # add 300ms buffer
        durations.append(sc["duration"])
        print(f"  Scene {idx+1} ({sc['id']}): {sc['duration']:.2f}s")
        
    # Concat all scene audios into master_voiceover.wav
    concat_txt = os.path.join(ASSETS_DIR, "concat.txt")
    with open(concat_txt, "w") as f:
        for idx in range(len(SCENES_DATA)):
            f.write(f"file scene_{idx}.mp3\n")
            
    subprocess.run(
        [ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c:a", "pcm_s16le", MASTER_AUDIO],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print(f"Master voiceover created: {MASTER_AUDIO} (Total duration: {sum(durations):.2f}s)")

def capture_ui_views():
    os.makedirs(ASSETS_DIR, exist_ok=True)
    port = 8780
    web_dir = os.path.abspath("app")
    handler = lambda *args, **kwargs: http.server.SimpleHTTPRequestHandler(*args, directory=web_dir, **kwargs)
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    print("Capturing responsive UI screenshots with Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 430, "height": 920}, device_scale_factor=2)
        page.goto(f"http://127.0.0.1:{port}/static/index.html")
        page.wait_for_timeout(1500)

        # 0. Intro
        page.screenshot(path=os.path.join(ASSETS_DIR, "snap_intro.png"))

        # 1. Blueprint (Ideas)
        page.screenshot(path=os.path.join(ASSETS_DIR, "snap_blueprint.png"))

        # 2. Budget
        page.evaluate("switchTab('budget')")
        page.wait_for_timeout(600)
        page.screenshot(path=os.path.join(ASSETS_DIR, "snap_budget.png"))

        # 3. Timeline
        page.evaluate("switchTab('timeline')")
        page.wait_for_timeout(600)
        page.screenshot(path=os.path.join(ASSETS_DIR, "snap_timeline.png"))

        # 4. Chat
        page.evaluate("switchTab('chat')")
        page.wait_for_timeout(600)
        page.screenshot(path=os.path.join(ASSETS_DIR, "snap_genie.png"))

        # 5. Outro / Export Modal
        page.evaluate("openExportModal()")
        page.wait_for_timeout(600)
        page.screenshot(path=os.path.join(ASSETS_DIR, "snap_outro.png"))

        browser.close()

    httpd.shutdown()
    print("All UI views captured successfully.")

class ParticleSystem:
    """Simulates warm golden bokeh particles drifting up for festive cinematic aesthetic."""
    def __init__(self, count=45):
        random.seed(42)
        self.particles = []
        for _ in range(count):
            self.particles.append({
                "x": random.uniform(20, WIDTH - 20),
                "y": random.uniform(0, HEIGHT),
                "radius": random.uniform(3, 14),
                "speed": random.uniform(0.6, 2.2),
                "drift": random.uniform(-0.4, 0.4),
                "color": random.choice([
                    (245, 158, 11, 40),  # Amber
                    (251, 191, 36, 50),  # Warm gold
                    (244, 63, 94, 35),   # Rose celebration
                    (236, 72, 153, 30),  # Pink festive
                ])
            })

    def update(self):
        for p in self.particles:
            p["y"] -= p["speed"]
            p["x"] += p["drift"]
            if p["y"] < -20:
                p["y"] = HEIGHT + random.uniform(10, 40)
                p["x"] = random.uniform(20, WIDTH - 20)

    def draw(self, img_draw):
        for p in self.particles:
            r = p["radius"]
            x, y = p["x"], p["y"]
            img_draw.ellipse(
                [(x - r, y - r), (x + r, y + r)],
                fill=p["color"][:3]
            )

def create_festive_background():
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    # Deep royal celebration gradient: dark indigo-black to deep ruby wine (#090d16 -> #240d21)
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(9 * (1 - ratio) + 36 * ratio)
        g = int(13 * (1 - ratio) + 13 * ratio)
        b = int(22 * (1 - ratio) + 33 * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
    return img

def render_cinematic_frame(base_bg, particles, ss_img, scene, scene_progress, total_progress):
    frame = base_bg.copy()
    draw = ImageDraw.Draw(frame)

    # 1. Draw floating festive particles
    particles.draw(draw)

    # 2. Top Header Title
    font_brand = get_font(32, bold=True)
    font_sub = get_font(18, bold=False)
    font_badge = get_font(18, bold=True)
    font_caption = get_font(21, bold=True)

    # Top Brand Ribbon
    draw.rounded_rectangle([(30, 42), (WIDTH - 30, 112)], radius=18, fill=(15, 23, 42, 230), outline=(244, 63, 94, 160), width=2)
    draw.text((WIDTH // 2, 63), "UTSAV AI  *  INDIAN EVENT COPILOT", fill=(255, 255, 255), font=font_brand, anchor="mm")
    draw.text((WIDTH // 2, 94), "Google Cloud x Hack2skill GenAI Hackathon", fill=(251, 191, 36), font=font_sub, anchor="mm")

    # 3. Dynamic Step Badge
    badge_w = 340
    draw.rounded_rectangle([(WIDTH // 2 - badge_w // 2, 130), (WIDTH // 2 + badge_w // 2, 170)], radius=14, fill=(16, 185, 129, 35), outline=(52, 211, 153), width=2)
    draw.text((WIDTH // 2, 150), scene["badge"], fill=(52, 211, 153), font=font_badge, anchor="mm")

    # 4. Phone Mockup with subtle pan animation
    phone_w, phone_h = 560, 800
    px = (WIDTH - phone_w) // 2
    py = 188

    # Outer phone chassis
    draw.rounded_rectangle([(px - 7, py - 7), (px + phone_w + 7, py + phone_h + 7)], radius=36, fill=(30, 41, 59), outline=(100, 116, 139), width=3)
    # Top dynamic notch
    draw.rounded_rectangle([(WIDTH // 2 - 45, py + 3), (WIDTH // 2 + 45, py + 20)], radius=8, fill=(15, 23, 42))

    # Calculate smooth vertical pan offset
    inner_w = phone_w
    inner_h = phone_h - 24
    ss_w, ss_h = ss_img.size
    
    # Crop with Ken Burns pan down
    max_pan = max(0, int(ss_h * 0.15))
    pan_y = int(max_pan * scene_progress)
    
    crop_box = (0, pan_y, ss_w, min(ss_h, int(ss_w * (inner_h / inner_w)) + pan_y))
    cropped = ss_img.crop(crop_box).resize((inner_w, inner_h), Image.Resampling.LANCZOS)
    frame.paste(cropped, (px, py + 24))

    # 5. Live Cinematic Subtitle Pill
    draw.rounded_rectangle([(32, 1010), (WIDTH - 32, 1130)], radius=20, fill=(10, 15, 30, 245), outline=(245, 158, 11, 180), width=2)
    
    # Subtitle text wrapped
    sub_text = scene["subtitle"]
    # Wrap text if long
    words = sub_text.split()
    line1, line2 = "", ""
    for w in words:
        if len(line1) + len(w) < 38:
            line1 += (w + " ")
        else:
            line2 += (w + " ")
            
    draw.text((WIDTH // 2, 1045), line1.strip(), fill=(255, 255, 255), font=font_caption, anchor="mm")
    if line2:
        draw.text((WIDTH // 2, 1085), line2.strip(), fill=(251, 191, 36), font=font_caption, anchor="mm")

    # 6. Bottom Sticky Branding Pill
    draw.rounded_rectangle([(32, 1148), (WIDTH - 32, 1228)], radius=16, fill=(15, 23, 42, 230), outline=(71, 85, 105), width=2)
    draw.text((WIDTH // 2, 1172), "🚀 Powered by Gemini 2.5 • FastAPI • Python", fill=(244, 63, 94), font=get_font(18, bold=True), anchor="mm")
    draw.text((WIDTH // 2, 1204), "github.com/jafarali32/event-planner-ai-india", fill=(148, 163, 184), font=get_font(16, bold=False), anchor="mm")

    # 7. Bottom glowing progress bar
    bar_y = 1250
    draw.line([(32, bar_y), (WIDTH - 32, bar_y)], fill=(51, 65, 85), width=5)
    prog_x = int(32 + (WIDTH - 64) * total_progress)
    draw.line([(32, bar_y), (prog_x, bar_y)], fill=(244, 63, 94), width=5)

    return frame

def render_cinematic_video():
    total_duration = sum(sc["duration"] for sc in SCENES_DATA)
    total_frames = int(total_duration * FPS)
    print(f"Rendering cinematic video: {total_duration:.2f}s ({total_frames} frames @ {FPS} FPS)...")

    base_bg = create_festive_background()
    particles = ParticleSystem(count=45)

    # Load screenshots
    ss_map = {
        "intro": Image.open(os.path.join(ASSETS_DIR, "snap_intro.png")).convert("RGB"),
        "blueprint": Image.open(os.path.join(ASSETS_DIR, "snap_blueprint.png")).convert("RGB"),
        "budget": Image.open(os.path.join(ASSETS_DIR, "snap_budget.png")).convert("RGB"),
        "timeline": Image.open(os.path.join(ASSETS_DIR, "snap_timeline.png")).convert("RGB"),
        "genie": Image.open(os.path.join(ASSETS_DIR, "snap_genie.png")).convert("RGB"),
        "outro": Image.open(os.path.join(ASSETS_DIR, "snap_outro.png")).convert("RGB"),
    }

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(TEMP_VIDEO, fourcc, float(FPS), (WIDTH, HEIGHT))

    current_frame = 0
    for sc in SCENES_DATA:
        scene_frames = int(sc["duration"] * FPS)
        ss_img = ss_map[sc["id"]]

        for f in range(scene_frames):
            particles.update()
            scene_progress = f / max(1, scene_frames)
            total_progress = current_frame / max(1, total_frames)

            frame_pil = render_cinematic_frame(
                base_bg=base_bg,
                particles=particles,
                ss_img=ss_img,
                scene=sc,
                scene_progress=scene_progress,
                total_progress=total_progress,
            )
            cv_frame = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)
            out.write(cv_frame)
            current_frame += 1

    out.release()
    print("Video frame rendering complete. Muxing audio & video...")

    # Mux video + master audio using bundled FFmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg, "-y",
        "-i", TEMP_VIDEO,
        "-i", MASTER_AUDIO,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        FINAL_VIDEO
    ]
    subprocess.run(cmd, check=True)
    if os.path.exists(TEMP_VIDEO):
        os.remove(TEMP_VIDEO)

    print(f"SUCCESS: Created {FINAL_VIDEO} ({os.path.getsize(FINAL_VIDEO)/(1024*1024):.2f} MB)")

def main():
    asyncio.run(generate_voiceovers())
    capture_ui_views()
    render_cinematic_video()

if __name__ == "__main__":
    main()
