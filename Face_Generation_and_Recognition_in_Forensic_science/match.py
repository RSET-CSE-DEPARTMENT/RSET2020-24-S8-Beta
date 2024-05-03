import os
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.models import Model
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Load VGG16 model
base_model = VGG16(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)


# Function to extract features from an image
def extract(img):
    img = img.resize((224, 224))  # Resize the image
    img = img.convert('RGB')  # Convert the image color space
    x = image.img_to_array(img)  # Reformat the image
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    feature = model.predict(x)  # Extract Features
    return feature / np.linalg.norm(feature)


# Function to find the top 2 similar images for a query image
def find_top_similar_images(query_features, dataset_features):
    dists = np.linalg.norm(dataset_features - query_features, axis=1)  # Calculate the similarity (distance) between images
    similarity_percentage = 100 - (dists / dists.max()) * 100  # Calculate similarity percentage
    ids = np.argsort(dists)[:2]  # Extract 2 images that have the lowest distance
    return ids, similarity_percentage[ids]


# Path to the dataset folder
folder_path = 'dataset'

# Load features for all images in the dataset
images = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if
          file.endswith(('.jpg', '.jpeg', '.png'))]
all_features = np.zeros(shape=(len(images), 4096))
for i in range(len(images)):
    feature = extract(img=Image.open(images[i]))
    all_features[i] = np.array(feature)

# Path to the query image
query_path = r'D:\college\Projects\pythonProject\bald.jpeg'

# Extract features of the query image
query_features = extract(img=Image.open(query_path))

# Find the top 2 similar images in the dataset
similar_image_ids, similarity_percentages = find_top_similar_images(query_features, all_features)

# Plot the query image
plt.figure(figsize=(8, 4))
plt.subplot(1, 3, 1)
plt.imshow(Image.open(query_path))
plt.title("Query Image")
plt.axis('off')

# Plot the top 2 similar images
for i, img_id in enumerate(similar_image_ids, 2):
    img_path = images[img_id]
    img = Image.open(img_path)

    plt.subplot(1, 3, i)
    plt.imshow(img)
    plt.title(f'Similarity: {similarity_percentages[i - 2]:.2f}%')
    plt.axis('off')

plt.tight_layout()
plt.show()
