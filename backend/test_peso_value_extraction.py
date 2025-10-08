#!/usr/bin/env python3
"""
Test peso value extraction from detection class names
"""
import os
import sys

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def extract_peso_value(class_name: str) -> str:
    """Extract peso denomination value from detection class name"""
    class_lower = class_name.lower()
    
    print(f"Processing class name: {class_name} -> {class_lower}")
    
    # Extract peso values from various detection names with priority order
    # Check larger denominations first to avoid conflicts (e.g., "1000" before "100")
    if "1000" in class_lower:
        return "1000"
    elif "500" in class_lower:
        return "500"
    elif "200" in class_lower:
        return "200"
    elif "100" in class_lower:
        return "100"
    elif "50" in class_lower:
        return "50"
    elif "20" in class_lower and "200" not in class_lower:
        return "20"
    elif "10" in class_lower and "100" not in class_lower and "1000" not in class_lower:
        return "10"
    elif "5" in class_lower and "50" not in class_lower and "500" not in class_lower:
        return "5"
    elif "1" in class_lower and "10" not in class_lower and "100" not in class_lower and "1000" not in class_lower:
        return "1"
    else:
        return "unknown"

def test_peso_value_extraction():
    """Test peso value extraction with various class names"""
    test_cases = [
        # Actual YOLOv8 model class names from our model
        "1000_pearl",
        "1000_pearl_watermark", 
        "100_whale",
        "100_whale_watermark",
        "20_New_Front",
        "20_New_Back",
        "20_civet",
        "20_civet_watermark",
        "50_maliputo",
        "50_maliputo_watermark",
        "500_big_parrot",
        "500_parrot_watermark",
        "10_New_Back",
        "10_New_Front",
        "10_Old_Back",
        "10_Old_Front",
        "5_New_Back",
        "5_New_Front",
        "5_Old_Back",
        "5_Old_Front",
        "1_New_Back",
        "1_New_Front",
        "1_Old_Back",
        "1_Old_Front",
        "200_tarsier",
        "200_tarsier_watermark",
        
        # Security features (should return "unknown")
        "watermark",
        "security_thread",
        "concealed_value",
        "optically_variable_device",
        "sampaguita",
        "eagle",
        "serial_number",
        "value",
        "value_watermark",
        
        # Edge cases
        "clear_window",
        "see_through_mark",
        "unknown_feature"
    ]
    
    print("🧪 TESTING PESO VALUE EXTRACTION")
    print("=" * 60)
    
    peso_values_found = {}
    
    for class_name in test_cases:
        peso_value = extract_peso_value(class_name)
        print(f"📝 {class_name:<25} -> ₱{peso_value}")
        
        if peso_value != "unknown":
            if peso_value not in peso_values_found:
                peso_values_found[peso_value] = []
            peso_values_found[peso_value].append(class_name)
    
    print("\n" + "=" * 60)
    print("🏆 PESO DENOMINATIONS DETECTED:")
    print("=" * 60)
    
    # Sort peso values numerically
    sorted_values = sorted(peso_values_found.keys(), key=lambda x: int(x))
    
    for peso_value in sorted_values:
        detections = peso_values_found[peso_value]
        print(f"💰 ₱{peso_value} PESO: {len(detections)} detections")
        for detection in detections:
            print(f"   - {detection}")
    
    print(f"\n✅ Total peso denominations detected: {len(peso_values_found)}")
    print(f"📊 Available denominations: {', '.join([f'₱{v}' for v in sorted_values])}")

if __name__ == "__main__":
    test_peso_value_extraction()