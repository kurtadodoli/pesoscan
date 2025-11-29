#!/usr/bin/env python3
"""
Convert the PesoScan SVG logo to PNG format
"""

import os
import sys
from pathlib import Path

def create_png_logo():
    """Create a PNG version of the PesoScan logo"""
    try:
        # Try using cairosvg if available
        try:
            import cairosvg
            
            svg_path = Path(__file__).parent / "public" / "logo192.svg"
            png_path = Path(__file__).parent / "public" / "logo.png"
            
            print(f"Converting {svg_path} to {png_path}")
            
            with open(svg_path, 'r') as svg_file:
                svg_content = svg_file.read()
            
            # Convert SVG to PNG
            cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), 
                           write_to=str(png_path),
                           output_width=192,
                           output_height=192)
            
            print(f"✅ Successfully created PNG logo: {png_path}")
            return True
            
        except ImportError:
            print("cairosvg not available, trying alternative method...")
            
        # Alternative: Use PIL/Pillow to create the logo programmatically
        try:
            from PIL import Image, ImageDraw, ImageFont
            import math
            
            # Create a 192x192 image
            size = 192
            image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            
            # Create gradient background circle
            center = size // 2
            radius = 90
            
            # Draw the circle with gradient effect (simplified)
            for i in range(radius, 0, -1):
                # Calculate gradient color from blue to lighter blue
                ratio = i / radius
                r = int(30 + (59 - 30) * (1 - ratio))
                g = int(58 + (130 - 58) * (1 - ratio))
                b = int(138 + (246 - 138) * (1 - ratio))
                
                draw.ellipse([center - i, center - i, center + i, center + i], 
                           fill=(r, g, b, 255))
            
            # Draw outer stroke
            draw.ellipse([center - radius, center - radius, center + radius, center + radius], 
                        outline=(251, 191, 36, 255), width=4)
            
            # Try to add peso symbol and text
            try:
                # Try to load a font
                font_large = ImageFont.truetype("arial.ttf", 80)
                font_small = ImageFont.truetype("arial.ttf", 16)
            except:
                try:
                    font_large = ImageFont.load_default()
                    font_small = ImageFont.load_default()
                except:
                    font_large = None
                    font_small = None
            
            if font_large:
                # Draw peso symbol
                draw.text((center, center + 10), "₱", font=font_large, 
                         fill=(251, 191, 36, 255), anchor="mm")
                
                # Draw "SCAN" text
                draw.text((center, center + 55), "SCAN", font=font_small, 
                         fill=(251, 191, 36, 255), anchor="mm")
            
            # Save the image
            png_path = Path(__file__).parent / "public" / "logo.png"
            image.save(png_path, 'PNG')
            
            print(f"✅ Successfully created PNG logo: {png_path}")
            return True
            
        except ImportError:
            print("PIL/Pillow not available")
            
        # Final fallback: Create a simple colored circle
        print("Using basic fallback method...")
        
        # Create a simple HTML canvas approach via a different method
        # This creates a basic representation
        
        return False
        
    except Exception as e:
        print(f"Error creating PNG logo: {e}")
        return False

if __name__ == "__main__":
    success = create_png_logo()
    if not success:
        print("Could not create PNG logo automatically.")
        print("You can convert the SVG to PNG using online tools like:")
        print("- https://convertio.co/svg-png/")
        print("- https://cloudconvert.com/svg-to-png")
        print("Or install cairosvg: pip install cairosvg")