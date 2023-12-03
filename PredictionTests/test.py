from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

# Replace with your prediction key, endpoint, and iteration ID
prediction_key = '57c136b1236d443f89ed61930650c2ac'
endpoint = 'https://ssammodel.cognitiveservices.azure.com/'
iteration_id = 'd3e519ac-e430-4c5a-a237-d14481fdade3'
project_id = '73a72cbd-0f0d-41cb-868a-375773a4e186'
training_key = '349956367fa24a27b7868f83929155de'

# Create prediction client
training_credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
training_client = CustomVisionTrainingClient(endpoint=endpoint, credentials=training_credentials)
credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
prediction_client = CustomVisionPredictionClient(endpoint=endpoint, credentials=credentials)

# Replace with the actual image file path
image_path = 'test.JPG'

# Read image data
with open(image_path, 'rb') as image_data:
    # Classify the image
    results = prediction_client.classify_image(project_id, iteration_id, image_data.read())

    # Assuming the model is a classification model
    predictions = results.predictions
    top_prediction = predictions[0]
    predicted_label = top_prediction.tag_name
    confidence = top_prediction.probability

    print(f"Predicted Label: {predicted_label}")
    print(f"Confidence: {confidence}")