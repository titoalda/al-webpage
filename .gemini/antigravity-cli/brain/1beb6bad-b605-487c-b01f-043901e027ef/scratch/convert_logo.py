from PIL import Image
import os

logo_src = "/home/vboxuser/al-webpage/MI LOGO-02.png"
logo_dest = "/home/vboxuser/al-webpage/static/images/mi_logo.png"
favicon_dest = "/home/vboxuser/al-webpage/favicon.ico"

print("Opening source image:", logo_src)
if os.path.exists(logo_src):
    img = Image.open(logo_src)
    
    # 1. Save PNG copy to static/images/mi_logo.png
    os.makedirs(os.path.dirname(logo_dest), exist_ok=True)
    img.save(logo_dest, "PNG")
    print("Saved PNG copy to:", logo_dest)
    
    # 2. Convert to favicon.ico with standard resolutions (16x16, 32x32, 48x48)
    img.save(favicon_dest, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
    print("Saved optimized favicon.ico to:", favicon_dest)
else:
    print("Error: Source image not found at", logo_src)
