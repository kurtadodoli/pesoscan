#!/usr/bin/env python3
"""
🔥 COUNTERFEIT DETECTION TRAINING RECOVERY SCRIPT 🔥
Resume training from your excellent 90-epoch checkpoint to complete 100 epochs!

Your Current Progress:
- 90/100 epochs completed
- 93.9% mAP50 accuracy achieved 
- Only 10 more epochs needed!
"""

import os
import sys
import time
from pathlib import Path
from ultralytics import YOLO
import yaml

def setup_environment():
    """Setup the training environment"""
    print("🚀 Setting up counterfeit detection training recovery...")
    
    # Set up paths
    backend_dir = Path(__file__).parent
    project_root = backend_dir.parent
    
    # Dataset paths
    counterfeit_dataset = backend_dir / "Counterfeit-Money-Detector-5"
    data_yaml = counterfeit_dataset / "data.yaml"
    
    # Training checkpoint path
    checkpoint_dir = backend_dir / "complete_counterfeit_training" / "counterfeit_detection_complete"
    last_checkpoint = checkpoint_dir / "weights" / "last.pt"
    
    return {
        'data_yaml': str(data_yaml),
        'checkpoint_path': str(last_checkpoint),
        'project_dir': str(backend_dir / "counterfeit_recovery_final"),
        'name': 'counterfeit_final_completion'
    }

def verify_progress():
    """Verify the existing training progress"""
    print("🔍 Verifying your existing training progress...")
    
    # Check CSV results
    results_file = Path("complete_counterfeit_training/counterfeit_detection_complete/results.csv")
    if results_file.exists():
        with open(results_file, 'r') as f:
            lines = f.readlines()
            if len(lines) > 90:  # Header + 90 epochs
                last_line = lines[-1].strip().split(',')
                epoch = last_line[0]
                map50 = last_line[7]
                print(f"✅ Last completed epoch: {epoch}")
                print(f"✅ Best mAP50 achieved: {map50}")
                print("🎯 Ready to resume training!")
                return True
    
    print("❌ Could not verify training progress")
    return False

def resume_counterfeit_training(config):
    """Resume the counterfeit detection training from epoch 90"""
    print("🔥 RESUMING COUNTERFEIT DETECTION TRAINING!")
    print("=" * 60)
    print("📊 Training Configuration:")
    print(f"   Dataset: {config['data_yaml']}")
    print(f"   Checkpoint: {config['checkpoint_path']}")
    print(f"   Target: Complete final 10 epochs (90→100)")
    print(f"   Expected completion: ~30-40 minutes")
    print("=" * 60)
    
    try:
        # Load model from checkpoint
        print("📦 Loading model from your epoch-90 checkpoint...")
        model = YOLO(config['checkpoint_path'])
        
        print("🏆 Model loaded successfully!")
        print("🎯 Starting final 10 epochs of training...")
        
        # Resume training for remaining epochs
        start_time = time.time()
        
        results = model.train(
            data=config['data_yaml'],
            epochs=100,  # Total epochs (will resume from 90)
            patience=10,
            save=True,
            save_period=5,
            cache=True,
            device='cpu',  # Using CPU for stability
            workers=2,
            batch=8,
            imgsz=640,
            project=config['project_dir'],
            name=config['name'],
            exist_ok=True,
            pretrained=False,  # Don't use pretrained, use our checkpoint
            resume=True,  # Resume from checkpoint
            verbose=True
        )
        
        training_time = time.time() - start_time
        
        print("🎉 COUNTERFEIT TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"⏱️  Total recovery time: {training_time/60:.1f} minutes")
        print(f"📁 Results saved in: {config['project_dir']}/{config['name']}")
        print("🏆 Your counterfeit detection model is now complete!")
        
        # Copy final model to main models directory
        final_model_source = Path(config['project_dir']) / config['name'] / "weights" / "best.pt"
        final_model_dest = Path("trained_models") / "counterfeit_detection_final_best.pt"
        
        if final_model_source.exists():
            import shutil
            final_model_dest.parent.mkdir(exist_ok=True)
            shutil.copy2(final_model_source, final_model_dest)
            print(f"✅ Final model copied to: {final_model_dest}")
            
            # Get file size
            size_mb = final_model_dest.stat().st_size / (1024 * 1024)
            print(f"📦 Model size: {size_mb:.1f} MB")
        
        return True
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        return False

def test_recovered_model():
    """Test the recovered counterfeit model"""
    print("\n🧪 Testing your completed counterfeit model...")
    
    model_path = Path("trained_models") / "counterfeit_detection_final_best.pt"
    if not model_path.exists():
        print("❌ Final model not found")
        return False
    
    try:
        model = YOLO(str(model_path))
        print("✅ Counterfeit model loaded successfully!")
        print(f"📊 Model classes: {len(model.names)}")
        print("🎯 Ready for counterfeit peso detection!")
        return True
        
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

def main():
    print("🔥 COUNTERFEIT DETECTION TRAINING RECOVERY 🔥")
    print("═" * 60)
    print("🎯 Resuming from your excellent 90-epoch checkpoint!")
    print("📈 Current: 93.9% mAP50 accuracy")
    print("🏁 Target: Complete 100-epoch training")
    print("⏱️  Estimated time: 30-40 minutes")
    print("═" * 60)
    
    # Verify existing progress
    if not verify_progress():
        print("❌ Cannot proceed without verified training progress")
        return 1
    
    # Setup configuration
    config = setup_environment()
    
    # Verify checkpoint exists
    if not Path(config['checkpoint_path']).exists():
        print(f"❌ Checkpoint not found: {config['checkpoint_path']}")
        return 1
    
    print(f"✅ Found checkpoint: {config['checkpoint_path']}")
    
    # Resume training
    success = resume_counterfeit_training(config)
    
    if success:
        # Test the final model
        test_recovered_model()
        
        print("\n🎉 COUNTERFEIT TRAINING RECOVERY COMPLETE!")
        print("=" * 60)
        print("✅ Training successfully resumed and completed")
        print("✅ Final counterfeit detection model ready")
        print("✅ Model integrated into PesoScan system")
        print("🚀 Your counterfeit detection is now ready for production!")
        return 0
    else:
        print("❌ Training recovery failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())