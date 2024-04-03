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


    def computeImageFeatures(self, image_urls):
        images = []
        for url in image_urls:
            images.append(Image.open(requests.get(url, stream=True).raw))
        inputs = self.processor(images=images, return_tensors="pt")
        outputs = self.model.get_image_features(**inputs).tolist()
        #print(outputs)
        #session['image_features'] = outputs
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


'''
 def findImages(self, search, image_urls):
        images = []
        for url in image_urls:
            images.append(Image.open(requests.get(url, stream=True).raw))
        
        inputs = self.processor(text=search, images=images, return_tensors="pt", padding=True)

        outputs = self.model(**inputs)
        logits_per_image = outputs.logits_per_image  # this is the image-text similarity score
        probs = logits_per_image.softmax(dim=1)  #  softmax to get the label probabilities
        return outputs


'''