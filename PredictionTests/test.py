# Testing script to predict different images via URLs

from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

# Replace with project values
key = ''
endpoint = ''
project_id = ''

credentials = ApiKeyCredentials(in_headers={"Prediction-key": key})
prediction_client = CustomVisionPredictionClient(endpoint=endpoint, credentials=credentials)

while True:
    itChoice = input("Which iteration would you like to use? (1, 2 or 'quit' to quit): ")
    if itChoice == '1':
        iteration_id = 'Iteration1'
    elif itChoice == '2':
        iteration_id = 'Iteration3'
    elif itChoice == 'quit':
        break

    print(f"Using {iteration_id}...\n")
    
    image_url = input("Enter the image URL: ")

    results = prediction_client.classify_image_url(project_id, iteration_id, image_url)

    predictions = results.predictions

    if predictions:
        top_prediction = predictions[0]
        predicted_label = top_prediction.tag_name
        confidence = top_prediction.probability

        print(f"Predicted Label: {predicted_label}")
        print(f"Confidence: {confidence}")
    else:
        print("No predictions were returned for the given image.")
