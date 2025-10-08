#!/usr/bin/env python3
"""
Create multiple PNG sizes of the PesoScan logo
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_logo_png(size, filename):
    """Create a PNG logo of specified size"""
    try:
        # Create image
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Scale elements based on size
        center = size // 2
        radius = int(size * 0.47)  # 90/192 ratio
        stroke_width = max(1, int(size * 0.02))  # 4/192 ratio
        
        # Draw gradient circle
        for i in range(radius, 0, -1):
            ratio = i / radius
            r = int(30 + (59 - 30) * (1 - ratio))
            g = int(58 + (130 - 58) * (1 - ratio))
            b = int(138 + (246 - 138) * (1 - ratio))
            
            draw.ellipse([center - i, center - i, center + i, center + i], 
                       fill=(r, g, b, 255))
        
        # Draw outer stroke
        draw.ellipse([center - radius, center - radius, center + radius, center + radius], 
                    outline=(251, 191, 36, 255), width=stroke_width)
        
        # Try to add text
        try:
            font_large_size = int(size * 0.42)  # 80/192 ratio
            font_small_size = int(size * 0.08)  # 16/192 ratio
            
            try:
                font_large = ImageFont.truetype("arial.ttf", font_large_size)
                font_small = ImageFont.truetype("arial.ttf", font_small_size)
            except:
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Draw peso symbol
            y_offset_peso = int(size * 0.05)  # Slight offset down
            draw.text((center, center + y_offset_peso), "₱", font=font_large, 
                     fill=(251, 191, 36, 255), anchor="mm")
            
            # Draw "SCAN" text if there's room
            if size >= 48:
                y_offset_scan = int(size * 0.29)  # Position below peso symbol
                draw.text((center, center + y_offset_scan), "SCAN", font=font_small, 
                         fill=(251, 191, 36, 255), anchor="mm")
        
        except Exception as e:
            print(f"Warning: Could not add text to {size}x{size} logo: {e}")
        
        # Save the image
        png_path = Path(__file__).parent / "public" / filename
        image.save(png_path, 'PNG')
        print(f"✅ Created {filename} ({size}x{size})")
        return True
        
    except Exception as e:
        print(f"Error creating {filename}: {e}")
        return False

def create_all_logo_sizes():
    """Create various PNG sizes of the logo"""
    sizes = [
        (16, "logo-16.png"),
        (32, "logo-32.png"), 
        (48, "logo-48.png"),
        (64, "logo-64.png"),
        (96, "logo-96.png"),
        (128, "logo-128.png"),
        (192, "logo-192.png"),
        (256, "logo-256.png"),
        (512, "logo-512.png")
    ]
    
    print("Creating multiple PNG logo sizes...")
    
    for size, filename in sizes:
        create_logo_png(size, filename)
    
    print(f"✅ Created {len(sizes)} PNG logo sizes!")

if __name__ == "__main__":
    create_all_logo_sizes()