"""
Monitor Counterfeit Detection Training Progress
Check the status of the training process and model availability
"""

import os
import time
import glob
from datetime import datetime

def check_training_progress():
    """Check the progress of counterfeit detection training"""
    print("🔍 Checking Counterfeit Detection Training Progress")
    print("=" * 60)
    print(f"📅 Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check for training directories
    training_dirs = [
        "counterfeit_detection_runs/counterfeit_yolov8_v2",
        "counterfeit_detection_runs/counterfeit_yolov8_train"
    ]
    
    active_training = False
    
    for train_dir in training_dirs:
        if os.path.exists(train_dir):
            print(f"\n📁 Found training directory: {train_dir}")
            
            # Check for weights
            weights_dir = os.path.join(train_dir, "weights")
            if os.path.exists(weights_dir):
                weight_files = os.listdir(weights_dir)
                print(f"🏋️ Weight files: {weight_files}")
                
                # Check for best.pt
                best_pt = os.path.join(weights_dir, "best.pt")
                if os.path.exists(best_pt):
                    size = os.path.getsize(best_pt) / (1024*1024)  # MB
                    mtime = os.path.getmtime(best_pt)
                    mod_time = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                    print(f"✅ best.pt found: {size:.1f} MB (modified: {mod_time})")
                else:
                    print("⏳ best.pt not found yet - training in progress")
                    active_training = True
            
            # Check for results.csv (training log)
            results_csv = os.path.join(train_dir, "results.csv")
            if os.path.exists(results_csv):
                try:
                    with open(results_csv, 'r') as f:
                        lines = f.readlines()
                        if len(lines) > 1:  # Header + at least one data line
                            last_line = lines[-1].strip()
                            parts = last_line.split(',')
                            if len(parts) > 0:
                                epoch = parts[0].strip()
                                print(f"📊 Latest epoch: {epoch}")
                                if len(parts) > 4:
                                    try:
                                        train_loss = float(parts[3])
                                        val_loss = float(parts[4]) if len(parts) > 4 else "N/A"
                                        print(f"📈 Training loss: {train_loss:.4f}")
                                        print(f"📉 Validation loss: {val_loss}")
                                    except:
                                        pass
                except Exception as e:
                    print(f"⚠️ Could not read results.csv: {e}")
            
            # Check for plots
            plots = glob.glob(os.path.join(train_dir, "*.png"))
            if plots:
                print(f"📈 Training plots available: {len(plots)} files")
    
    # Check for model files in main directory
    print(f"\n🎯 Checking for completed models:")
    model_files = [
        "counterfeit_detection_model_v2.pt",
        "counterfeit_detection_model.pt"
    ]
    
    for model_file in model_files:
        if os.path.exists(model_file):
            size = os.path.getsize(model_file) / (1024*1024)  # MB
            mtime = os.path.getmtime(model_file)
            mod_time = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            print(f"✅ {model_file}: {size:.1f} MB (created: {mod_time})")
        else:
            print(f"⏳ {model_file}: Not available yet")
    
    # Check dataset
    print(f"\n📊 Dataset Status:")
    dataset_path = "Counterfeit-Money-Detector-5"
    if os.path.exists(dataset_path):
        print(f"✅ Dataset found at: {dataset_path}")
        
        # Check folder sizes
        for folder in ['train', 'valid', 'test']:
            images_path = os.path.join(dataset_path, folder, 'images')
            if os.path.exists(images_path):
                count = len([f for f in os.listdir(images_path) if f.endswith('.jpg')])
                print(f"📷 {folder}: {count} images")
    else:
        print(f"❌ Dataset not found")
    
    return not active_training

def monitor_training_loop():
    """Monitor training progress in a loop"""
    print("🔄 Starting training monitor (press Ctrl+C to stop)")
    
    try:
        while True:
            completed = check_training_progress()
            
            if completed:
                print("\n🎉 Training appears to be completed!")
                print("✅ Model should be ready for use in the backend")
                break
            else:
                print("\n⏳ Training still in progress...")
                print("💤 Checking again in 60 seconds...")
                time.sleep(60)
    
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--monitor":
        monitor_training_loop()
    else:
        check_training_progress()