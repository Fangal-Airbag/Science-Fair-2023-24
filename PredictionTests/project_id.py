from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from msrest.authentication import ApiKeyCredentials

# Replace with your training key and endpoint
training_key = '349956367fa24a27b7868f83929155de'
endpoint = 'https://ssammodel.cognitiveservices.azure.com/'
project_id = '73a72cbd-0f0d-41cb-868a-375773a4e186'

# Replace with your published iteration name
published_iteration_name = 'Iteration3'

# Create a training client
credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
training_client = CustomVisionTrainingClient(endpoint=endpoint, credentials=credentials)

# Get the iterations for the specified project
iterations = training_client.get_iterations(project_id)

latest_iteration = next((iteration for iteration in iterations if iteration.publish_name == 'Production'), None)

if latest_iteration:
    iteration_id = latest_iteration.id
    print(f"Latest Published Iteration ID: {iteration_id}")
else:
    print("No published iterations found.")