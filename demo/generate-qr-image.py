#!/usr/bin/env python3
"""
Generate QR Code Image for CENTLI
Creates a high-quality QR code PNG file
"""

try:
    import qrcode
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call(['pip3', 'install', 'qrcode[pil]', 'pillow'])
    import qrcode
    from PIL import Image, ImageDraw, ImageFont

# Configuration
URL = "https://d210pgg1e91kn6.cloudfront.net"
OUTPUT_FILE = "centli-qr-code.png"

# Create QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

qr.add_data(URL)
qr.make(fit=True)

# Create image with custom colors
img = qr.make_image(fill_color="#667eea", back_color="white")

# Convert to RGB for adding text
img = img.convert('RGB')

# Create a larger canvas with space for text
width, height = img.size
new_height = height + 200
new_img = Image.new('RGB', (width, new_height), 'white')

# Paste QR code
new_img.paste(img, (0, 0))

# Add text
draw = ImageDraw.Draw(new_img)

# Try to use a nice font, fallback to default
try:
    title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
    url_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
    subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 25)
except:
    title_font = ImageFont.load_default()
    url_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()

# Add title
title = "CENTLI"
title_bbox = draw.textbbox((0, 0), title, font=title_font)
title_width = title_bbox[2] - title_bbox[0]
title_x = (width - title_width) // 2
draw.text((title_x, height + 20), title, fill="#667eea", font=title_font)

# Add subtitle
subtitle = "Asistente Financiero Inteligente"
subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
subtitle_x = (width - subtitle_width) // 2
draw.text((subtitle_x, height + 90), subtitle, fill="#666666", font=subtitle_font)

# Add URL
url_text = "d210pgg1e91kn6.cloudfront.net"
url_bbox = draw.textbbox((0, 0), url_text, font=url_font)
url_width = url_bbox[2] - url_bbox[0]
url_x = (width - url_width) // 2
draw.text((url_x, height + 140), url_text, fill="#1976d2", font=url_font)

# Save image
new_img.save(OUTPUT_FILE, quality=95)

print(f"✅ QR Code generated: {OUTPUT_FILE}")
print(f"📱 URL: {URL}")
print(f"📐 Size: {width}x{new_height} pixels")
print(f"\nYou can now:")
print(f"  - Open {OUTPUT_FILE} to view")
print(f"  - Use in presentations")
print(f"  - Print for physical demos")
print(f"  - Share on social media")
