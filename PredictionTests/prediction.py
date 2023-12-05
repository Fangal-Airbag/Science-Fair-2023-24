# Script to get different common AI scores and graphs on a testing set

from os import listdir
from os.path import isfile, join
import time
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
from sklearn.metrics import precision_score, recall_score, f1_score, roc_curve, auc, precision_recall_curve
import matplotlib.pyplot as plt

# Replace with project values
endpoint = ''
key = ''
project_id = ''

confidence_threshold = 0.5

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": key})
prediction_client = CustomVisionPredictionClient(endpoint=endpoint, credentials=prediction_credentials)

def get_image_paths(folder_path):
    return [join(folder_path, f) for f in listdir(folder_path) if isfile(join(folder_path, f))]

def evaluate_folder(folder_path, ground_truth_label, max_retries=3, retry_delay=5):
    image_paths = get_image_paths(folder_path)
    true_labels = []
    predicted_scores = []

    for image_path in image_paths:
        for attempt in range(max_retries):
            try:
                with open(image_path, 'rb') as image_data:
                    results = prediction_client.classify_image(project_id, iteration_id, image_data.read())
                    predictions = results.predictions
                    top_prediction = predictions[0]
                    predicted_score = top_prediction.probability
                    predicted_label = top_prediction.tag_name

                    if predicted_score < confidence_threshold:
                        predicted_label = [p.tag_name for p in predictions if p.tag_name != predicted_label][0]

                    true_labels.append(1 if predicted_label == ground_truth_label else 0)
                    predicted_scores.append(predicted_score)

                    print(f"Image: {image_path}, Predicted Label: {predicted_label}, Confidence: {predicted_score}")

                    break
            except Exception as e:
                print(f"Error in attempt {attempt + 1}: {e}")
                time.sleep(retry_delay)
    
    precision = precision_score(true_labels, [1 if score >= confidence_threshold else 0 for score in predicted_scores])
    recall = recall_score(true_labels, [1 if score >= confidence_threshold else 0 for score in predicted_scores])
    f_score = f1_score(true_labels, [1 if score >= confidence_threshold else 0 for score in predicted_scores])

    print(f"Precision for {ground_truth_label}: {precision}")
    print(f"Recall for {ground_truth_label}: {recall}")
    print(f"F-score for {ground_truth_label}: {f_score}")

    return true_labels, predicted_scores

def plot_roc_curve(true_labels, predicted_scores, label_name):
    fpr, tpr, thresholds = roc_curve(true_labels, predicted_scores, drop_intermediate=False)
    roc_auc = auc(fpr, tpr)

    plt.figure()
    plt.plot(fpr, tpr, label=f'{label_name} (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlabel('False Positive Rate (FPR)')
    plt.ylabel('True Positive Rate (TPR)')
    plt.title(f'Receiver Operating Characteristic (ROC) Curve for {label_name} - (Iteration 1)')
    plt.legend(loc="lower right")
    plt.show()

def plot_precision_recall_curve(true_labels, predicted_scores, label_name):
    precision, recall, thresholds = precision_recall_curve(true_labels, predicted_scores)
    area_under_curve = auc(recall, precision)

    plt.figure()
    plt.plot(recall, precision, label=f'Precision-Recall curve (AUC = {area_under_curve:.2f})')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title(f'Precision-Recall Curve for {label_name} - (Iteration 1)')
    plt.legend(loc="lower right")
    plt.show()

# Iteration 3 was a typo, it is the second iteration :P
itChoice = input("Which iteration would you like to use? (1 or 2): ")
if itChoice == '1':
    iteration_id = 'Iteration1'
elif itChoice == '2':
    iteration_id = 'Iteration3'

print(f"Using {iteration_id}...\n")

# Replace with your folder paths
benign_folder_path = 'D:/ScienceFair/Science-Fair-2023-24/Data/benign'
malignant_folder_path = 'D:/ScienceFair/Science-Fair-2023-24/Data/malignant'

true_labels_benign, predicted_scores_benign = evaluate_folder(benign_folder_path, 'benign')
true_labels_malignant, predicted_scores_malignant = evaluate_folder(malignant_folder_path, 'malignant')

plot_roc_curve(true_labels_benign, predicted_scores_benign, label_name='benign')
plot_roc_curve(true_labels_malignant, predicted_scores_malignant, label_name='malignant')

plot_precision_recall_curve(true_labels_benign, predicted_scores_benign, label_name='benign')
plot_precision_recall_curve(true_labels_malignant, predicted_scores_malignant, label_name='malignant')