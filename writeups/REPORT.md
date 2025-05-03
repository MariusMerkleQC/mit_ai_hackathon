## 1. Challenge

I choose to solve challenge 5 (Anomaly Detection for Thermal Drone Footage), applied to identify missing persons. I have tackled the approach beyond anomaly detection, as classifying which image is abnormal is far from sufficient. Ultimately, a rescue team needs to decide what path to take to find a missing person. Therefore, the output of my model is a path that maximizes the chance to find a missing person.

## 2. Tools / ML models you have used

### 2.1 Dataset

I used the provided dataset provided by the Black Forest Mountain Rescue Team. The dataset consists of 166 training images (all are normal without a missing person) and 60 test images (30 are normal and 30 are abnormal (with a missing person)). The images had no GPS location in their metadata, so I generated random GPS coordinates within the Black Forest in Germany for each image.

### 2.2 Modeling Approach

I tackled this challenge using a "predict-then-optimize" approach:

1. **Feature Extraction**: I extracted image embeddings using the penultimate layer of the pre-trained ResNet18 model.
2. **Prediction (anomaly detection)**: After extracting embeddings from all 226 images, I used the k-nearest neighbors (kNN) algorithm to compute the mean distance of each test image to its 5 nearest neighbors in the training set.
3. **Optimization**: The image distance scores serve as an _input_ to the optimization problem. The goal is to maximize the sum of image distance scores (proxy for the probability of finding a missing person), while constraining the total distance traveled by the rescue team (proxy for available time).

## 3. What has worked well with these tools?

The pre-trained RestNet18 model provided a powerful feature extractor, as it was trained on a large dataset (ImageNet) and is capable of capturing complex patterns in images. The optimization problem could also be solved efficiently using integer programming.

## 4. What was challenging?

The most challenging part is computing the distance scores for the test images. With 512 dimensions, the distance scores start suffering from the curse of dimensionality.

## 5. How have you spent your time?

Overall, I could only work for 5 hours on this challenge, as I feel quite sick and had to sleep for 10 hours overnight. I spent
- 30 minutes on understanding the challenge
- 3 hours on the technical implementation (1 hour for each of the three steps: feature extraction, prediction, and optimization)
- 1.5 hours on writing the report, summary and recording the videos