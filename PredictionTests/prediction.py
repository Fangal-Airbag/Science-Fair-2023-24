import os
from os import listdir
from os.path import isfile, join
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

# Retrieve values from environment variables
endpoint = 'https://ssammodel.cognitiveservices.azure.com/' #os.environ["VISION_TRAINING_ENDPOINT"]
prediction_endpoint = 'https://ssammodel-prediction.cognitiveservices.azure.com/'
training_key = '349956367fa24a27b7868f83929155de'
prediction_key = '57c136b1236d443f89ed61930650c2ac' #os.environ["VISION_PREDICTION_KEY"]
project_id = '73a72cbd-0f0d-41cb-868a-375773a4e186' #os.environ["VISION_PREDICTION_RESOURCE_ID"]
iteration_id = 'd3e519ac-e430-4c5a-a237-d14481fdade3' #os.environ["VISION_ITERATION_ID"]

# VISION_TRAINING_ENDPOINT https://ssammodel.cognitiveservices.azure.com/
# VISION_PREDICTION_KEY 57c136b1236d443f89ed61930650c2ac
# VISION_PREDICTION_RESOURCE_ID /subscriptions/0e7daf8d-1dbb-449f-b902-2a834c51e50f/resourceGroups/ScienceFair/providers/Microsoft.CognitiveServices/accounts/SSAMMODEL-Prediction
# VISION_ITERATION_ID d3e519ac-e430-4c5a-a237-d14481fdade3

training_credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
training_client = CustomVisionTrainingClient(endpoint=endpoint, credentials=training_credentials)
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
prediction_client = CustomVisionPredictionClient(endpoint=prediction_endpoint, credentials=prediction_credentials)

# Function to evaluate a single image
def evaluate_image(image_path):
    with open(image_path, 'rb') as image_data:
        results = prediction_client.classify_image(project_id, iteration_id, image_data.read())
        # Assuming the model is a classification model
        predictions = results.predictions
        top_prediction = predictions[0]
        predicted_label = top_prediction.tag_name
        confidence = top_prediction.probability
        return predicted_label, confidence

# Function to get all image paths from a folder
def get_image_paths(folder_path):
    return [join(folder_path, f) for f in listdir(folder_path) if isfile(join(folder_path, f))]

# Function to evaluate images from a folder
def evaluate_folder(folder_path, ground_truth_label):
    image_paths = get_image_paths(folder_path)
    correct_predictions = 0
    total_images = len(image_paths)

    for image_path in image_paths:
        predicted_label, confidence = evaluate_image(image_path)
        is_correct = predicted_label == ground_truth_label
        if is_correct:
            correct_predictions += 1
        print(f"Image: {image_path}, Predicted Label: {predicted_label}, Confidence: {confidence}")

    accuracy_percentage = (correct_predictions / total_images) * 100
    print(f"Accuracy for {ground_truth_label}: {accuracy_percentage}%")

# Replace with your folder paths
benign_folder_path = 'D:/ScienceFair/Science-Fair-2023-24/Data/benign'
malignant_folder_path = 'D:/ScienceFair/Science-Fair-2023-24/Data/malignant'

# Evaluate images from benign folder
evaluate_folder(benign_folder_path, 'benign')

# Evaluate images from malignant folder
evaluate_folder(malignant_folder_path, 'malignant')
