from PIL import Image
import requests
from transformers import CLIPProcessor, CLIPModel
from IPython.display import display
import torch
import numpy as np
from flask import session

# Assuming text_features and image_feature are 2D numpy arrays


class MediaManager:
    
    def __init__(self, app):
        self.app = app
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    
    def findImages(self, search, image_urls, count):
        features = self.computeImageFeatures(image_urls)
        similarity = self.imageSimilarity(search, features)
        sorted_pairs = sorted(zip(image_urls, similarity), key=lambda x: x[1], reverse=True)
        sorted_image_urls = [url for url, score in sorted_pairs][:count]
        top_5_pairs = sorted_pairs[:5]
        for pair in top_5_pairs:
            print(f"Similarity: {pair[1]}")
        
        return sorted_image_urls
    
    def applyDataSearch(self, search, data, count):
        similarity = self.imageSimilarity(search, data['features'])
        sorted_pairs = sorted(zip(data['image_urls'], similarity), key=lambda x: x[1], reverse=True)
        sorted_image_urls = [url for url, score in sorted_pairs][:count]
        top_5_pairs = sorted_pairs[:5]
        return sorted_image_urls
        
        return sorted_image_urls
    # create list of image urls and feature vectors
    def processImages(self, image_urls):
        features = self.computeImageFeatures(image_urls)
        return {'image_urls': image_urls, 'features':features}


    def computeImageFeatures(self, image_urls):
        images = []
        for url in image_urls:
            images.append(Image.open(requests.get(url, stream=True).raw))
        inputs = self.processor(images=images, return_tensors="pt")
        outputs = self.model.get_image_features(**inputs).tolist()
        return outputs
    

    def imageSimilarity(self, query, stored_image_features):

        stored_image_features = torch.tensor(stored_image_features)
        text_inputs = self.processor(text=[query], return_tensors="pt", padding=True)
        text_features = self.model.get_text_features(**text_inputs)
        similarities = [self.cosine_similarity(text_features, image_feature).tolist() for image_feature in stored_image_features]


        return similarities


    def cosine_similarity(self, text_features, image_features):

        if text_features.ndim == 1:
            text_features = text_features.unsqueeze(0)

        return torch.nn.functional.cosine_similarity(text_features, image_features, dim=1)

