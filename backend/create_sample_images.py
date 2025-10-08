#!/usr/bin/env python3
"""
Create sample Philippine peso bill images for testing PesoScan
This generates synthetic representations for demo purposes
"""

import os
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

def create_peso_bill_image(denomination, width=400, height=200):
    """Create a synthetic Philippine peso bill image"""
    
    # Color schemes for different denominations
    colors = {
        20: {'bg': '#8B4513', 'text': '#FFFFFF', 'accent': '#DAA520'},     # Brown
        50: {'bg': '#FF4500', 'text': '#FFFFFF', 'accent': '#FFD700'},     # Orange-Red
        100: {'bg': '#8A2BE2', 'text': '#FFFFFF', 'accent': '#FF69B4'},    # Purple
        200: {'bg': '#008000', 'text': '#FFFFFF', 'accent': '#90EE90'},    # Green
        500: {'bg': '#FFD700', 'text': '#8B4513', 'accent': '#FFA500'},    # Gold
        1000: {'bg': '#000080', 'text': '#FFFFFF', 'accent': '#87CEEB'}    # Navy Blue
    }
    
    color_scheme = colors.get(denomination, colors[100])  # Default to 100 peso colors
    
    # Create image
    img = Image.new('RGB', (width, height), color_scheme['bg'])
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font (fallback to default if not available)
    try:
        # Try to load a TrueType font
        font_large = ImageFont.truetype("arial.ttf", 36)
        font_medium = ImageFont.truetype("arial.ttf", 24)
        font_small = ImageFont.truetype("arial.ttf", 16)
    except:
        # Fallback to default font
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Main denomination text
    draw.text((width//2, height//2 - 30), f"₱{denomination}", 
              fill=color_scheme['text'], font=font_large, anchor="mm")
    
    # "PISO" text
    draw.text((width//2, height//2 + 10), "PISO", 
              fill=color_scheme['text'], font=font_medium, anchor="mm")
    
    # "BANGKO SENTRAL NG PILIPINAS" text
    draw.text((width//2, 30), "BANGKO SENTRAL NG PILIPINAS", 
              fill=color_scheme['text'], font=font_small, anchor="mm")
    
    # Serial number
    draw.text((20, height - 30), f"AA123456{denomination}", 
              fill=color_scheme['accent'], font=font_small)
    
    # Year
    draw.text((width - 80, height - 30), "2024", 
              fill=color_scheme['accent'], font=font_small)
    
    # Border
    draw.rectangle([5, 5, width-5, height-5], outline=color_scheme['accent'], width=3)
    
    # Decorative elements
    # Corner decorations
    for x, y in [(15, 15), (width-35, 15), (15, height-35), (width-35, height-35)]:
        draw.ellipse([x, y, x+20, y+20], fill=color_scheme['accent'])
    
    return img

def create_sample_images():
    """Create sample Philippine peso images"""
    logger.info("🏦 Creating Sample Philippine Peso Images")
    logger.info("=" * 50)
    
    # Create directories
    images_dir = Path("sample_images")
    images_dir.mkdir(exist_ok=True)
    
    dataset_dir = Path("datasets/philippine-money-hjn3v-1")
    
    # Create test images directory in dataset
    test_images_dir = dataset_dir / "test" / "images"
    test_images_dir.mkdir(parents=True, exist_ok=True)
    
    valid_images_dir = dataset_dir / "valid" / "images"
    valid_images_dir.mkdir(parents=True, exist_ok=True)
    
    # Philippine peso denominations
    denominations = [20, 50, 100, 200, 500, 1000]
    
    created_files = []
    
    for denom in denominations:
        logger.info(f"💵 Creating {denom} peso bill images...")
        
        # Create multiple variations for each denomination
        for i in range(3):
            # Different sizes and orientations
            if i == 0:  # Standard size
                img = create_peso_bill_image(denom, 400, 200)
                filename = f"peso_{denom}_standard_{i+1}.png"
            elif i == 1:  # Slightly rotated/different size
                img = create_peso_bill_image(denom, 380, 190)
                filename = f"peso_{denom}_variant_{i+1}.png"
            else:  # Another variation
                img = create_peso_bill_image(denom, 420, 210)
                filename = f"peso_{denom}_sample_{i+1}.png"
            
            # Save to sample images
            sample_path = images_dir / filename
            img.save(sample_path)
            created_files.append(sample_path)
            
            # Also save to dataset structure
            test_path = test_images_dir / filename
            img.save(test_path)
            
            # Save one to valid set too
            if i == 0:
                valid_path = valid_images_dir / filename
                img.save(valid_path)
            
            logger.info(f"  ✅ Created: {filename}")
    
    # Create a composite image showing all denominations
    logger.info("🖼️ Creating composite image...")
    composite_width = 1200
    composite_height = 800
    composite = Image.new('RGB', (composite_width, composite_height), '#F0F0F0')
    
    # Arrange bills in a 2x3 grid
    positions = [
        (50, 50),    # 20 peso
        (450, 50),   # 50 peso
        (850, 50),   # 100 peso
        (50, 350),   # 200 peso
        (450, 350),  # 500 peso
        (850, 350)   # 1000 peso
    ]
    
    for i, denom in enumerate(denominations):
        bill_img = create_peso_bill_image(denom, 300, 150)
        composite.paste(bill_img, positions[i])
    
    # Add title
    draw = ImageDraw.Draw(composite)
    try:
        title_font = ImageFont.truetype("arial.ttf", 32)
    except:
        title_font = ImageFont.load_default()
    
    draw.text((composite_width//2, 25), "Philippine Peso Bills - PesoScan Demo", 
              fill='#333333', font=title_font, anchor="mm")
    
    composite_path = images_dir / "philippine_peso_collection.png"
    composite.save(composite_path)
    created_files.append(composite_path)
    
    logger.info(f"✅ Composite image created: {composite_path}")
    
    # Create labels for dataset (YOLO format)
    logger.info("🏷️ Creating YOLO labels...")
    
    labels_dir = dataset_dir / "test" / "labels"
    labels_dir.mkdir(parents=True, exist_ok=True)
    
    valid_labels_dir = dataset_dir / "valid" / "labels"
    valid_labels_dir.mkdir(parents=True, exist_ok=True)
    
    # Class mapping
    class_mapping = {20: 0, 50: 1, 100: 2, 200: 3, 500: 4, 1000: 5}
    
    for denom in denominations:
        class_id = class_mapping[denom]
        
        for i in range(3):
            if i == 0:
                filename = f"peso_{denom}_standard_{i+1}.txt"
            elif i == 1:
                filename = f"peso_{denom}_variant_{i+1}.txt"
            else:
                filename = f"peso_{denom}_sample_{i+1}.txt"
            
            # YOLO format: class_id x_center y_center width height (normalized)
            # For our synthetic images, the bill takes up most of the image
            label_content = f"{class_id} 0.5 0.5 0.9 0.8\n"
            
            # Save to test labels
            test_label_path = labels_dir / filename
            with open(test_label_path, 'w') as f:
                f.write(label_content)
            
            # Save to valid labels (first image only)
            if i == 0:
                valid_label_path = valid_labels_dir / filename
                with open(valid_label_path, 'w') as f:
                    f.write(label_content)
    
    # Update data.yaml
    data_yaml_content = f"""train: {dataset_dir / "train" / "images"}
val: {dataset_dir / "valid" / "images"}
test: {dataset_dir / "test" / "images"}

nc: 6
names: ['20-peso', '50-peso', '100-peso', '200-peso', '500-peso', '1000-peso']
"""
    
    with open(dataset_dir / "data.yaml", 'w') as f:
        f.write(data_yaml_content)
    
    logger.info("✅ YOLO labels created")
    logger.info("✅ data.yaml updated")
    
    logger.info(f"\n🎉 Sample images creation completed!")
    logger.info(f"📁 Created {len(created_files)} sample images")
    logger.info(f"📍 Sample images location: {images_dir}")
    logger.info(f"📍 Dataset location: {dataset_dir}")
    logger.info("\n📋 Files created:")
    for file_path in created_files:
        logger.info(f"  - {file_path}")
    
    return created_files

if __name__ == "__main__":
    created_files = create_sample_images()
    print(f"\n🏆 Successfully created {len(created_files)} sample Philippine peso images!")
    print("🔍 You can now test the PesoScan system with these images.")