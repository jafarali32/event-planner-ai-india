"""
Generate a professional 9:16 (720x1280) Instagram Reel MP4 video for Utsav AI.
"""
import os
import time
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

OUTPUT_DIR = "reel_assets"
VIDEO_PATH = "utsav_ai_instagram_reel.mp4"
WIDTH, HEIGHT = 720, 1280
FPS = 30

import http.server
import socketserver
import threading

def capture_screenshots():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Start temporary local HTTP server serving app directory
    port = 8765
    web_dir = os.path.abspath("app")
    handler = lambda *args, **kwargs: http.server.SimpleHTTPRequestHandler(*args, directory=web_dir, **kwargs)
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    
    print("Capturing UI screenshots via Playwright from local HTTP server...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 430, "height": 840}, device_scale_factor=2)
        page.goto(f"http://127.0.0.1:{port}/static/index.html")
        page.wait_for_timeout(1500)

        # 1. Main Ideas tab
        page.screenshot(path=os.path.join(OUTPUT_DIR, "01_ideas.png"))

        # 2. Budget tab
        page.evaluate("switchTab('budget')")
        page.wait_for_timeout(500)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "02_budget.png"))

        # 3. Timeline tab
        page.evaluate("switchTab('timeline')")
        page.wait_for_timeout(500)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "03_timeline.png"))

        # 4. Chat tab
        page.evaluate("switchTab('chat')")
        page.wait_for_timeout(500)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "04_chat.png"))

        browser.close()
    
    httpd.shutdown()
    print("Screenshots captured successfully.")

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

def create_base_canvas():
    """Create a gradient 720x1280 background."""
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    # Gradient from #0d1117 (dark blue/gray) to #261129 (deep celebration magenta/violet)
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(13 * (1 - ratio) + 38 * ratio)
        g = int(17 * (1 - ratio) + 17 * ratio)
        b = int(23 * (1 - ratio) + 41 * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
    return img

def render_frame(base_img, ss_img, title_text, badge_text, highlight_text, step_num, progress):
    """Render a single frame composed of mockup, headers, titles, and glowing cards."""
    frame = base_img.copy()
    draw = ImageDraw.Draw(frame)

    font_title = get_font(34, bold=True)
    font_sub = get_font(20, bold=False)
    font_badge = get_font(18, bold=True)
    font_card_title = get_font(22, bold=True)
    font_footer = get_font(18, bold=True)

    # 1. Top Header Banner
    draw.rounded_rectangle([(30, 40), (WIDTH - 30, 110)], radius=18, fill=(244, 63, 94, 25), outline=(244, 63, 94, 120), width=2)
    draw.text((WIDTH // 2, 60), "UTSAV AI - EVENT PLANNER", fill=(255, 255, 255), font=font_title, anchor="mm")
    draw.text((WIDTH // 2, 92), "Google Cloud x Hack2skill GenAI Hackathon | Challenge 5", fill=(251, 191, 36), font=font_sub, anchor="mm")

    # 2. Step Badge
    draw.rounded_rectangle([(WIDTH // 2 - 140, 130), (WIDTH // 2 + 140, 168)], radius=14, fill=(16, 185, 129, 40), outline=(16, 185, 129), width=2)
    draw.text((WIDTH // 2, 149), badge_text, fill=(52, 211, 153), font=font_badge, anchor="mm")

    # 3. Feature Highlight Card
    draw.rounded_rectangle([(40, 185), (WIDTH - 40, 255)], radius=16, fill=(15, 23, 42, 230), outline=(56, 189, 248, 140), width=2)
    draw.text((WIDTH // 2, 210), title_text, fill=(255, 255, 255), font=font_card_title, anchor="mm")
    draw.text((WIDTH // 2, 236), highlight_text, fill=(148, 163, 184), font=font_sub, anchor="mm")

    # 4. Phone Screen Mockup
    # Phone container: (WIDTH - 520)//2 = 100, Y from 275 to 1130
    phone_w, phone_h = 560, 840
    px = (WIDTH - phone_w) // 2
    py = 275

    # Phone outer frame
    draw.rounded_rectangle([(px - 8, py - 8), (px + phone_w + 8, py + phone_h + 8)], radius=36, fill=(30, 41, 59), outline=(71, 85, 105), width=3)
    # Notch / Camera island
    draw.rounded_rectangle([(WIDTH // 2 - 50, py + 4), (WIDTH // 2 + 50, py + 22)], radius=8, fill=(15, 23, 42))

    # Resize screenshot and paste inside phone frame
    resized_ss = ss_img.resize((phone_w, phone_h - 26), Image.Resampling.LANCZOS)
    frame.paste(resized_ss, (px, py + 26))

    # 5. Bottom Footer Callout
    draw.rounded_rectangle([(30, 1140), (WIDTH - 30, 1240)], radius=18, fill=(15, 23, 42, 240), outline=(244, 63, 94, 100), width=2)
    draw.text((WIDTH // 2, 1165), "Built with Google Gemini 2.5 & FastAPI", fill=(244, 63, 94), font=font_footer, anchor="mm")
    draw.text((WIDTH // 2, 1195), "Live App: event-planner-ai-india.onrender.com", fill=(255, 255, 255), font=font_sub, anchor="mm")
    draw.text((WIDTH // 2, 1222), "GitHub: github.com/jafarali32/event-planner-ai-india", fill=(148, 163, 184), font=get_font(15), anchor="mm")

    # 6. Progress bar at very bottom
    bar_y = 1265
    draw.line([(30, bar_y), (WIDTH - 30, bar_y)], fill=(51, 65, 85), width=4)
    prog_x = int(30 + (WIDTH - 60) * progress)
    draw.line([(30, bar_y), (prog_x, bar_y)], fill=(244, 63, 94), width=4)

    return frame

def build_reel_video():
    capture_screenshots()

    scenes = [
        {
            "img": os.path.join(OUTPUT_DIR, "01_ideas.png"),
            "badge": "STEP 1 - AI BLUEPRINT",
            "title": "Culturally-Aware Event Plans in Seconds",
            "highlight": "Sangeet, Muhurtham, Mehndi & Reception blueprints",
            "duration_sec": 3.5,
        },
        {
            "img": os.path.join(OUTPUT_DIR, "02_budget.png"),
            "badge": "STEP 2 - BUDGET MAESTRO",
            "title": "Real-Time INR (₹) Expense Tracking",
            "highlight": "Automated vendor allocation, variance & savings",
            "duration_sec": 3.5,
        },
        {
            "img": os.path.join(OUTPUT_DIR, "03_timeline.png"),
            "badge": "STEP 3 - RUN OF SHOW",
            "title": "Minute-by-Minute Day-of Timelines",
            "highlight": "Baraat entry, Varmala, Puja, dinner & live cues",
            "duration_sec": 3.5,
        },
        {
            "img": os.path.join(OUTPUT_DIR, "04_chat.png"),
            "badge": "STEP 4 - EVENTGENIE AI",
            "title": "Empathetic 24/7 AI Wedding Assistant",
            "highlight": "Vendor negotiation, inquiry drafting & contingency planning",
            "duration_sec": 4.5,
        },
    ]

    total_duration = sum(s["duration_sec"] for s in scenes)
    total_frames = int(total_duration * FPS)
    print(f"Generating video: {total_duration}s ({total_frames} frames at {FPS} FPS)...")

    base_canvas = create_base_canvas()
    loaded_images = [Image.open(s["img"]).convert("RGB") for s in scenes]

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(VIDEO_PATH, fourcc, float(FPS), (WIDTH, HEIGHT))

    current_frame = 0
    for scene_idx, scene in enumerate(scenes):
        scene_frames = int(scene["duration_sec"] * FPS)
        ss_img = loaded_images[scene_idx]

        for f in range(scene_frames):
            progress = current_frame / total_frames
            frame_pil = render_frame(
                base_img=base_canvas,
                ss_img=ss_img,
                title_text=scene["title"],
                badge_text=scene["badge"],
                highlight_text=scene["highlight"],
                step_num=scene_idx + 1,
                progress=progress,
            )
            # Convert PIL to BGR OpenCV format
            cv_frame = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)
            out.write(cv_frame)
            current_frame += 1

    out.release()
    file_size_mb = os.path.getsize(VIDEO_PATH) / (1024 * 1024)
    print(f"SUCCESS: Created {VIDEO_PATH} ({file_size_mb:.2f} MB)")

if __name__ == "__main__":
    build_reel_video()
