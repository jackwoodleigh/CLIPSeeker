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
    

    # computes similarity between vectors
    def cosine_similarity(self, text_features, image_features):
        if text_features.ndim == 1:
            text_features = text_features.unsqueeze(0)
        return torch.nn.functional.cosine_similarity(text_features, image_features, dim=1)
    


    # computes feature vector for one image
    def computeImageFeature(self, image_url):
        image = Image.open(requests.get(image_url, stream=True).raw)
        inputs = self.processor(images=image, return_tensors="pt")
        outputs = self.model.get_image_features(**inputs)
        return outputs


    
    def loadNewFeatureData(self, feature_data, photo_data):
        for fileid in photo_data.keys():
            if fileid not in feature_data:
                feature_data[fileid] = self.computeImageFeature(photo_data[fileid])
        return feature_data
    
    def searchImages(self, search, photos, features, count):
        similarity = self.findSimilarities(search, features)
        sorted_result  = sorted(similarity, key=lambda x: x[1][0], reverse=True)
        select = [item[0] for item in sorted_result [:count]]
        images = [photos[id] for id in select]
        return images

    def findSimilarities(self, query, features):
        '''for k, v in features.items():
            print(f"type v: {type(v[0])}")'''
        text_inputs = self.processor(text=[query], return_tensors="pt", padding=True)
        text_features = self.model.get_text_features(**text_inputs)
        similarities = [[fileid, self.cosine_similarity(text_features, torch.tensor(feature))] for fileid, feature in features.items()]
        return similarities

     

'''similarities = []
        for fileid, feature_list in features.items():
            # Convert feature_list to a tensor if it's not already one
            if not isinstance(feature_list, torch.Tensor):
                feature_tensor = torch.tensor(feature_list, dtype=torch.float)
            else:
                feature_tensor = feature_list

            similarity = self.cosine_similarity(text_features, feature_tensor)
            similarities.append([fileid, similarity])
            
            
            
            
    def findImages(self, search, image_urls, count):
        features = self.computeImageFeatures(image_urls)
        similarity = self.imageSimilarity(search, features)
        sorted_pairs = sorted(zip(image_urls, similarity), key=lambda x: x[1], reverse=True)
        sorted_image_urls = [url for url, score in sorted_pairs][:count]
        top_5_pairs = sorted_pairs[:5]
        for pair in top_5_pairs:
            print(f"Similarity: {pair[1]}")
        
        return sorted_image_urls
    

    # apply search to data
    def applyDataSearch(self, search, data, count):
        similarity = self.imageSimilarity(search, data['features'])
        sorted_pairs = sorted(zip(data['image_urls'], similarity), key=lambda x: x[1], reverse=True)
        sorted_image_urls = [url for url, score in sorted_pairs][:count]
        top_5_pairs = sorted_pairs[:5]
        return sorted_image_urls
    

    # create list of image urls and feature vectors
    def processImages(self, image_urls):
        features = self.computeImageFeatures(image_urls)
        return {'image_urls': image_urls, 'features':features}

    # computes feature vectors for all images
    def computeImageFeatures(self, image_urls):
        images = []
        for url in image_urls:
            images.append(Image.open(requests.get(url, stream=True).raw))
        inputs = self.processor(images=images, return_tensors="pt")
        outputs = self.model.get_image_features(**inputs).tolist()
        return outputs
    
    # computes similarity between text and image features
    def imageSimilarity(self, query, stored_image_features):

        stored_image_features = torch.tensor(stored_image_features)
        text_inputs = self.processor(text=[query], return_tensors="pt", padding=True)
        text_features = self.model.get_text_features(**text_inputs)
        similarities = [self.cosine_similarity(text_features, image_feature).tolist() for image_feature in stored_image_features]
        return similarities
            
            
            
            
            
            
            
            
            
            '''