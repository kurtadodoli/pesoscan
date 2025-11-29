"""
Sensitivity Analysis for Model Performance
Displays formatted tables of model metrics similar to research papers
"""

def print_object_detection_analysis():
    """Print Table 29: Summary of Sensitivity Analysis Results for Object Detection Algorithms"""
    
    # Object Detection trials data
    trials_data = [
        {"trial": 1, "yolov8": 9.90, "yolov7": 8.87, "yolov5": 8.83},
        {"trial": 2, "yolov8": 9.90, "yolov7": 8.88, "yolov5": 8.78},
        {"trial": 3, "yolov8": 9.90, "yolov7": 8.90, "yolov5": 8.72},
        {"trial": 4, "yolov8": 9.90, "yolov7": 8.91, "yolov5": 8.67},
        {"trial": 5, "yolov8": 9.90, "yolov7": 8.93, "yolov5": 8.61},
        {"trial": 6, "yolov8": 9.89, "yolov7": 8.99, "yolov5": 8.55},
    ]
    
    print("\n" + "="*100)
    print("TABLE 29: SENSITIVITY ANALYSIS")
    print("Summary of Sensitivity Analysis Results for Object Detection Algorithms")
    print("="*100)
    
    # Print table header
    header = f"{'Trial':^10} | {'YOLOv8':^15} | {'YOLOv7':^15} | {'YOLOv5':^15}"
    print(header)
    print("-"*100)
    
    # Print each trial's results
    for trial in trials_data:
        row = f"{trial['trial']:^10} | {trial['yolov8']:^15.2f} | {trial['yolov7']:^15.2f} | {trial['yolov5']:^15.2f}"
        print(row)
    
    print("="*100)
    
    # Calculate averages
    avg_yolov8 = sum(t['yolov8'] for t in trials_data) / len(trials_data)
    avg_yolov7 = sum(t['yolov7'] for t in trials_data) / len(trials_data)
    avg_yolov5 = sum(t['yolov5'] for t in trials_data) / len(trials_data)
    
    print(f"\n{'Average':^10} | {avg_yolov8:^15.2f} | {avg_yolov7:^15.2f} | {avg_yolov5:^15.2f}")
    
    # Find best performing algorithm
    best_algo = max([
        ("YOLOv8", avg_yolov8),
        ("YOLOv7", avg_yolov7),
        ("YOLOv5", avg_yolov5)
    ], key=lambda x: x[1])
    
    print(f"\nBEST PERFORMING ALGORITHM: {best_algo[0]} (Average: {best_algo[1]:.2f})")
    print("="*100 + "\n")


def print_classification_analysis():
    """Print Table 30: Summary of Sensitivity Analysis Results for Classification Algorithms"""
    
    # Classification trials data
    trials_data = [
        {"trial": 1, "custom_cnn": 9.90, "mobilenetv3": 9.83, "resnet50": 9.76, "efficientnetv2": 9.76, "densenet201": 9.60, "vgg16": 9.19},
        {"trial": 2, "custom_cnn": 9.87, "mobilenetv3": 9.80, "resnet50": 9.72, "efficientnetv2": 9.74, "densenet201": 9.57, "vgg16": 9.10},
        {"trial": 3, "custom_cnn": 9.84, "mobilenetv3": 9.78, "resnet50": 9.70, "efficientnetv2": 9.72, "densenet201": 9.55, "vgg16": 9.08},
        {"trial": 4, "custom_cnn": 9.79, "mobilenetv3": 9.72, "resnet50": 9.64, "efficientnetv2": 9.66, "densenet201": 9.49, "vgg16": 9.02},
        {"trial": 5, "custom_cnn": 9.72, "mobilenetv3": 9.65, "resnet50": 9.58, "efficientnetv2": 9.60, "densenet201": 9.41, "vgg16": 8.95},
        {"trial": 6, "custom_cnn": 9.66, "mobilenetv3": 9.59, "resnet50": 9.50, "efficientnetv2": 9.52, "densenet201": 9.33, "vgg16": 8.85},
    ]
    
    print("\n" + "="*130)
    print("TABLE 30: SENSITIVITY ANALYSIS")
    print("Summary of Sensitivity Analysis Results for Classification Algorithms")
    print("="*130)
    
    # Print table header
    header = f"{'Trial':^8} | {'Custom CNN':^13} | {'MobileNetv3':^13} | {'ResNet-50':^13} | {'EfficientNet-V2':^16} | {'DenseNet-201':^14} | {'VGG-16':^10}"
    print(header)
    print("-"*130)
    
    # Print each trial's results
    for trial in trials_data:
        row = f"{trial['trial']:^8} | {trial['custom_cnn']:^13.2f} | {trial['mobilenetv3']:^13.2f} | {trial['resnet50']:^13.2f} | {trial['efficientnetv2']:^16.2f} | {trial['densenet201']:^14.2f} | {trial['vgg16']:^10.2f}"
        print(row)
    
    print("="*130)
    
    # Calculate averages
    avg_custom_cnn = sum(t['custom_cnn'] for t in trials_data) / len(trials_data)
    avg_mobilenetv3 = sum(t['mobilenetv3'] for t in trials_data) / len(trials_data)
    avg_resnet50 = sum(t['resnet50'] for t in trials_data) / len(trials_data)
    avg_efficientnetv2 = sum(t['efficientnetv2'] for t in trials_data) / len(trials_data)
    avg_densenet201 = sum(t['densenet201'] for t in trials_data) / len(trials_data)
    avg_vgg16 = sum(t['vgg16'] for t in trials_data) / len(trials_data)
    
    print(f"\n{'Average':^8} | {avg_custom_cnn:^13.2f} | {avg_mobilenetv3:^13.2f} | {avg_resnet50:^13.2f} | {avg_efficientnetv2:^16.2f} | {avg_densenet201:^14.2f} | {avg_vgg16:^10.2f}")
    
    # Find best performing algorithm
    best_algo = max([
        ("Custom CNN", avg_custom_cnn),
        ("MobileNetv3", avg_mobilenetv3),
        ("ResNet-50", avg_resnet50),
        ("EfficientNet-V2", avg_efficientnetv2),
        ("DenseNet-201", avg_densenet201),
        ("VGG-16", avg_vgg16)
    ], key=lambda x: x[1])
    
    print(f"\nBEST PERFORMING ALGORITHM: {best_algo[0]} (Average: {best_algo[1]:.2f})")
    print("="*130 + "\n")


def print_sensitivity_analysis():
    """Print both sensitivity analysis tables"""
    print_object_detection_analysis()
    print_classification_analysis()


if __name__ == "__main__":
    print_sensitivity_analysis()
