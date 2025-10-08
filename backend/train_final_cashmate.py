#!/usr/bin/env python3
"""
Final CashMate Training - Full Production Training
"""

import os
import sys
import time
from pathlib import Path
from ultralytics import YOLO

def main():
    """Run full CashMate training"""
    print("🇵🇭 CashMate Philippine Banknotes - FULL TRAINING")
    print("=" * 60)
    
    # Check dataset
    dataset_path = Path("backend/CASHMATE-PH-BANKNOTES-11/data.yaml")
    if not dataset_path.exists():
        dataset_path = Path("CASHMATE-PH-BANKNOTES-11/data.yaml")
    
    if not dataset_path.exists():
        print("❌ Dataset not found!")
        print("Please run the download script first.")
        return 1
    
    print(f"📁 Using dataset: {dataset_path}")
    
    # Training configurations
    configs = {
        1: (50, 'yolov8n.pt', 16, "Quick training - 50 epochs"),
        2: (100, 'yolov8n.pt', 16, "Standard training - 100 epochs"), 
        3: (150, 'yolov8s.pt', 12, "Extended training - 150 epochs"),
        4: (200, 'yolov8s.pt', 8, "Production training - 200 epochs")
    }
    
    print("Available training configurations:")
    for key, (epochs, model, batch, desc) in configs.items():
        print(f"{key}. {desc} ({model}, batch {batch})")
    
    try:
        choice = input("\nSelect configuration (1-4) [default: 2]: ").strip()
        
        if not choice:
            choice = "2"
        
        if choice not in ['1', '2', '3', '4']:
            print("Invalid choice! Using standard training.")
            choice = "2"
        
        epochs, model_path, batch_size, desc = configs[int(choice)]
        
        print(f"\n🎯 Selected: {desc}")
        print(f"📊 Epochs: {epochs}")
        print(f"🏗️ Model: {model_path}")
        print(f"📦 Batch size: {batch_size}")
        
        # Confirm training
        confirm = input(f"\nProceed with training? This will take approximately {epochs//10}-{epochs//5} minutes (y/N): ")
        if confirm.lower() != 'y':
            print("Training cancelled.")
            return 0
        
        print("\n" + "="*60)
        print("🚀 STARTING CASHMATE TRAINING")
        print("="*60)
        
        # Initialize model
        print(f"🤖 Loading {model_path}...")
        model = YOLO(model_path)
        
        # Start training
        start_time = time.time()
        
        results = model.train(
            data=str(dataset_path),
            epochs=epochs,
            imgsz=640,
            batch=batch_size,
            name="cashmate_production",
            patience=20,
            save=True,
            plots=True,
            val=True,
            device='cpu',  # Force CPU for compatibility
            verbose=True
        )
        
        end_time = time.time()
        training_time = (end_time - start_time) / 60
        
        print("\n" + "="*60)
        print("🎉 TRAINING COMPLETED!")
        print("="*60)
        print(f"⏱️ Total time: {training_time:.1f} minutes")
        
        # Find results
        runs_dir = Path("runs/train")
        latest_run = None
        
        if runs_dir.exists():
            runs = list(runs_dir.glob("cashmate_production*"))
            if runs:
                latest_run = max(runs, key=os.path.getctime)
        
        if latest_run:
            print(f"📁 Results: {latest_run}")
            
            # Check model files
            weights_dir = latest_run / "weights"
            if weights_dir.exists():
                best_pt = weights_dir / "best.pt"
                last_pt = weights_dir / "last.pt"
                
                if best_pt.exists():
                    size_mb = best_pt.stat().st_size / (1024 * 1024)
                    print(f"🏆 Best model: {best_pt} ({size_mb:.1f} MB)")
                
                if last_pt.exists():
                    size_mb = last_pt.stat().st_size / (1024 * 1024)
                    print(f"📝 Last model: {last_pt} ({size_mb:.1f} MB)")
            
            # Check results
            results_csv = latest_run / "results.csv"
            if results_csv.exists():
                try:
                    import pandas as pd
                    df = pd.read_csv(results_csv)
                    final_metrics = df.iloc[-1]
                    
                    print(f"\n📊 Final Results:")
                    if 'metrics/mAP50(B)' in df.columns:
                        print(f"   mAP@50: {final_metrics['metrics/mAP50(B)']:.3f}")
                    if 'metrics/mAP50-95(B)' in df.columns:
                        print(f"   mAP@50-95: {final_metrics['metrics/mAP50-95(B)']:.3f}")
                    
                except Exception as e:
                    print(f"⚠️ Could not read metrics: {e}")
        
        print(f"\n🚀 Next Steps:")
        print("1. Test the model: python backend/test_cashmate_detection.py")
        print("2. Start the API: python backend/main.py")
        print("3. Use the test server: python backend/test_cashmate_server.py")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⏹️ Training interrupted!")
        return 1
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)