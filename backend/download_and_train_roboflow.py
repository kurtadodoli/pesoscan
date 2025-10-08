#!/usr/bin/env python3
"""
Download Counterfeit Money Detector dataset from Roboflow and train YOLOv8 model
"""

import os
from roboflow import Roboflow
from ultralytics import YOLO
import torch

# Step 1: Download dataset from Roboflow
api_key = "gZGoQuvlmBgBLq1Ev4Ar"
workspace = "aileen-crpev"
project_name = "counterfeit-money-detector"
version_num = 5
output_dir = "Counterfeit-Money-Detector-v5"

print("🔗 Connecting to Roboflow...")
rf = Roboflow(api_key=api_key)
project = rf.workspace(workspace).project(project_name)
version = project.version(version_num)
dataset = version.download("yolov8", location=output_dir)
print(f"✅ Dataset downloaded to: {output_dir}")

# Step 2: Train YOLOv8 model
print("\n🚀 Starting YOLOv8 training...")
device = "cuda" if torch.cuda.is_available() else "cpu"
model = YOLO('yolov8n.pt')

params = {
    'data': os.path.join(output_dir, 'data.yaml'),
    'epochs': 10,
    'imgsz': 416,
    'batch': 4,
    'device': device,
    'project': 'roboflow_runs',
    'name': 'counterfeit_money_v5',
    'save': True,
    'patience': 5,
    'verbose': True,
    'plots': True,
}

print("\n📋 Training Configuration:")
for key, value in params.items():
    print(f"  {key}: {value}")

results = model.train(**params)
print("\n✅ Training complete!")

# Step 3: Save best model
best_model_path = os.path.join('roboflow_runs', 'counterfeit_money_v5', 'weights', 'best.pt')
if os.path.exists(best_model_path):
    target_path = os.path.join(output_dir, 'counterfeit_money_v5_best.pt')
    os.rename(best_model_path, target_path)
    print(f"✓ Best model saved to: {target_path}")
else:
    print("❌ Best model not found after training.")

print("\n🎉 All steps completed!")
