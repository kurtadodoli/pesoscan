#!/usr/bin/env python3
"""
Test the updated counterfeit detection service with the new model
"""
import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.counterfeit_detection_service import CounterfeitDetectionService

async def test_counterfeit_service():
    """Test the counterfeit detection service"""
    print("🧪 Testing Updated Counterfeit Detection Service")
    print("="*50)
    
    try:
        # Initialize the service
        service = CounterfeitDetectionService()
        
        print("🔧 Initializing service...")
        await service.initialize()
        
        print(f"✅ Service initialized successfully!")
        print(f"📊 Model loaded: {service.model_loaded}")
        print(f"🗂️ Classes available: {len(service.counterfeit_class_mapping)}")
        
        if service.counterfeit_class_mapping:
            print("📝 Sample classes:")
            for i, (idx, class_name) in enumerate(list(service.counterfeit_class_mapping.items())[:10]):
                print(f"   {idx}: {class_name}")
            if len(service.counterfeit_class_mapping) > 10:
                print(f"   ... and {len(service.counterfeit_class_mapping) - 10} more classes")
        
        # Check if model is actually loaded
        if hasattr(service, 'counterfeit_model') and service.counterfeit_model:
            print(f"🤖 Model type: {type(service.counterfeit_model)}")
            print(f"🎯 Model ready for predictions!")
        else:
            print("⚠️ Model not loaded, running in basic mode")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing service: {e}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = asyncio.run(test_counterfeit_service())
    if success:
        print("\n🎉 SUCCESS! Counterfeit detection service is ready!")
    else:
        print("\n❌ FAILED! Service test encountered errors.")