"""
build_step_by_step_reel.py
Build an ultra-clean, professional Step-by-Step SaaS walkthrough reel:
- NO music (clean silent video)
- NO bokeh particles (clean modern dark product showcase)
- Focused step-by-step breakdown cards (Step 1 to Step 5)
- Sharp, high-resolution device framing showing the actual app
"""
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUTPUT_VIDEO = "utsav_ai_step_by_step_reel.mp4"
CINEMATIC_REPLACE = "utsav_ai_cinematic_reel.mp4"
WIDTH, HEIGHT = 720, 1280
FPS = 30

STEPS = [
    {
        "step_num": "STEP 1",
        "title": "Instant AI Event Blueprint",
        "desc": "Select wedding/celebration type & vibe. Gemini synthesizes themes, decor & rituals in seconds.",
        "img_path": "cinematic_assets/snap_blueprint.png",
        "duration": 5.0,
        "accent": (244, 63, 94), # Rose
    },
    {
        "step_num": "STEP 2",
        "title": "Budget Maestro (₹ INR)",
        "desc": "Automated rupee allocation across catering, venue & decor with live variance tracking.",
        "img_path": "cinematic_assets/snap_budget.png",
        "duration": 5.0,
        "accent": (16, 185, 129), # Emerald
    },
    {
        "step_num": "STEP 3",
        "title": "Minute-by-Minute Run of Show",
        "desc": "Day-of schedule syncing Baraat arrival, rituals, dinner & entertainment with zero confusion.",
        "img_path": "cinematic_assets/snap_timeline.png",
        "duration": 5.0,
        "accent": (59, 130, 246), # Blue
    },
    {
        "step_num": "STEP 4",
        "title": "EventGenie 24/7 AI Copilot",
        "desc": "Interactive chat powered by Gemini 2.5 to draft vendor inquiries & negotiate quotes.",
        "img_path": "cinematic_assets/snap_genie.png",
        "duration": 5.0,
        "accent": (245, 158, 11), # Amber
    },
    {
        "step_num": "STEP 5",
        "title": "1-Click PDF & Markdown Export",
        "desc": "Download complete raw JSON project backups or copy formatted Notion/Docs master briefs.",
        "img_path": "cinematic_assets/snap_outro.png",
        "duration": 5.0,
        "accent": (168, 85, 247), # Purple
    },
]

def get_font(size: int, bold: bool = False):
    font_names = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for fn in font_names:
        if os.path.exists(fn):
            try:
                return ImageFont.truetype(fn, size)
            except Exception:
                pass
    return ImageFont.load_default()

def create_clean_background():
    """Clean, modern dark studio background (#0b0f19 to #111827)."""
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(11 * (1 - ratio) + 17 * ratio)
        g = int(15 * (1 - ratio) + 24 * ratio)
        b = int(25 * (1 - ratio) + 39 * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
    return img

def render_step_frame(base_bg, step, ss_img, scene_prog, total_prog):
    frame = base_bg.copy()
    draw = ImageDraw.Draw(frame)

    font_title = get_font(26, bold=True)
    font_step = get_font(18, bold=True)
    font_desc = get_font(19, bold=False)
    font_brand = get_font(20, bold=True)
    font_meta = get_font(16, bold=False)

    accent_color = step["accent"]

    # 1. Top Brand Banner
    draw.rounded_rectangle([(30, 36), (WIDTH - 30, 96)], radius=14, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
    draw.text((WIDTH // 2, 53), "UTSAV AI  *  TOOL WALKTHROUGH", fill=(255, 255, 255), font=font_brand, anchor="mm")
    draw.text((WIDTH // 2, 79), "Step-by-Step Event Planner Demonstration", fill=(148, 163, 184), font=font_meta, anchor="mm")

    # 2. Step Header Card
    card_top = 110
    card_bot = 226
    draw.rounded_rectangle([(30, card_top), (WIDTH - 30, card_bot)], radius=16, fill=(15, 23, 42), outline=accent_color, width=2)

    # Step Badge Pill
    draw.rounded_rectangle([(46, card_top + 14), (160, card_top + 46)], radius=10, fill=accent_color)
    draw.text((103, card_top + 30), step["step_num"], fill=(255, 255, 255), font=font_step, anchor="mm")

    # Step Title
    draw.text((175, card_top + 30), step["title"], fill=(255, 255, 255), font=font_title, anchor="lm")

    # Step Explanation Subtext (wrapped)
    words = step["desc"].split()
    line1, line2 = "", ""
    for w in words:
        if len(line1) + len(w) < 42:
            line1 += (w + " ")
        else:
            line2 += (w + " ")

    draw.text((46, card_top + 68), line1.strip(), fill=(203, 213, 225), font=font_desc, anchor="lm")
    if line2:
        draw.text((46, card_top + 96), line2.strip(), fill=(148, 163, 184), font=font_desc, anchor="lm")

    # 3. Clean Device Frame (Focused App Screenshot)
    phone_w, phone_h = 580, 890
    px = (WIDTH - phone_w) // 2
    py = 246

    # Chassis
    draw.rounded_rectangle([(px - 4, py - 4), (px + phone_w + 4, py + phone_h + 4)], radius=24, fill=(30, 41, 59), outline=(71, 85, 105), width=2)
    # Screen
    ss_w, ss_h = ss_img.size
    inner_w, inner_h = phone_w, phone_h
    
    # Smooth subtle pan downward
    max_pan = max(0, int(ss_h * 0.12))
    pan_y = int(max_pan * scene_prog)
    
    crop_h = int(ss_w * (inner_h / inner_w))
    cropped = ss_img.crop((0, pan_y, ss_w, min(ss_h, crop_h + pan_y))).resize((inner_w, inner_h), Image.Resampling.LANCZOS)
    frame.paste(cropped, (px, py))

    # 4. Bottom Footer Info Card
    draw.rounded_rectangle([(30, 1156), (WIDTH - 30, 1228)], radius=14, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
    draw.text((WIDTH // 2, 1178), "Google Cloud Hackathon Challenge 5 • Built with Gemini 2.5", fill=(255, 255, 255), font=get_font(18, bold=True), anchor="mm")
    draw.text((WIDTH // 2, 1206), "Live: event-planner-ai-india.onrender.com  |  GitHub: jafarali32", fill=(148, 163, 184), font=font_meta, anchor="mm")

    # 5. Bottom Progress Bar
    bar_y = 1250
    draw.line([(30, bar_y), (WIDTH - 30, bar_y)], fill=(30, 41, 59), width=5)
    prog_x = int(30 + (WIDTH - 60) * total_prog)
    draw.line([(30, bar_y), (prog_x, bar_y)], fill=accent_color, width=5)

    return frame

def generate_step_by_step_reel():
    total_duration = sum(s["duration"] for s in STEPS)
    total_frames = int(total_duration * FPS)
    print(f"Building clean step-by-step walkthrough: {total_duration}s ({total_frames} frames @ {FPS} FPS)...")

    base_bg = create_clean_background()
    loaded_images = [Image.open(s["img_path"]).convert("RGB") for s in STEPS]

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, float(FPS), (WIDTH, HEIGHT))

    current_frame = 0
    for idx, step in enumerate(STEPS):
        scene_frames = int(step["duration"] * FPS)
        ss_img = loaded_images[idx]

        for f in range(scene_frames):
            scene_prog = f / max(1, scene_frames)
            total_prog = current_frame / max(1, total_frames)

            frame_pil = render_step_frame(
                base_bg=base_bg,
                step=step,
                ss_img=ss_img,
                scene_prog=scene_prog,
                total_prog=total_prog
            )
            cv_frame = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)
            out.write(cv_frame)
            current_frame += 1

    out.release()
    print("Video rendered successfully. Converting with ffmpeg...")

    # Convert to pure H.264 without audio stream using FFmpeg
    import subprocess, imageio_ffmpeg, shutil
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    clean_h264 = "clean_h264.mp4"
    cmd = [
        ffmpeg, "-y",
        "-i", OUTPUT_VIDEO,
        "-an", # Strictly NO audio stream
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        clean_h264
    ]
    subprocess.run(cmd, check=True)
    shutil.copyfile(clean_h264, OUTPUT_VIDEO)
    shutil.copyfile(clean_h264, CINEMATIC_REPLACE)
    os.remove(clean_h264)
    print(f"DONE: {OUTPUT_VIDEO} ({os.path.getsize(OUTPUT_VIDEO)/(1024*1024):.2f} MB)")

if __name__ == "__main__":
    generate_step_by_step_reel()
