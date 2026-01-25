import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import io
import numpy as np
from typing import List, Union
from app.config import settings

class ImageRecognitionService:
    def __init__(self):
        self.device = self._get_device()
        print(f"Initializing ImageRecognitionService on device: {self.device}")

        # Load MobileNetV3 Small
        self.model = models.mobilenet_v3_small(weights=models.MobileNet_V3_Small_Weights.DEFAULT)

        # Remove the classifier head to get embeddings
        # MobileNetV3 structure: features -> avgpool -> classifier
        # We want the output after avgpool (and squeeze)
        # However, forward method does: x = self.features(x) -> x = self.avgpool(x) -> x = torch.flatten(x, 1) -> x = self.classifier(x)
        # So we can replace classifier with Identity or just use the feature extractor part.
        # But keeping the full structure and replacing classifier is safer for structure.
        # actually, the classifier in v3 is a Sequential.
        # Let's just wrap it or modify it.
        # Replacing classifier with Identity works if we just want the pooled features.
        self.model.classifier = nn.Identity()

        self.model.to(self.device)
        self.model.eval()

        self.preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def _get_device(self):
        if settings.TORCH_DEVICE != "auto":
            return torch.device(settings.TORCH_DEVICE)

        if torch.cuda.is_available():
            return torch.device("cuda")
        elif torch.backends.mps.is_available():
            return torch.device("mps")
        else:
            return torch.device("cpu")

    def load_image(self, image_data: Union[str, bytes]) -> Image.Image:
        if isinstance(image_data, str):
            image = Image.open(image_data)
        elif isinstance(image_data, bytes):
            image = Image.open(io.BytesIO(image_data))
        else:
            raise ValueError("Unsupported image data type")

        if image.mode != "RGB":
            image = image.convert("RGB")
        return image

    def compute_embedding(self, image_data: Union[str, bytes]) -> List[float]:
        image = self.load_image(image_data)
        input_tensor = self.preprocess(image)
        input_batch = input_tensor.unsqueeze(0).to(self.device)

        with torch.no_grad():
            # Output of mobilenet_v3_small without classifier is 576 dimensional (for small)
            embedding = self.model(input_batch)
            # Flatten if needed
            embedding = torch.flatten(embedding, 1)

        return embedding.cpu().numpy()[0].tolist()

    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        # Cosine Similarity
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(np.dot(vec1, vec2) / (norm1 * norm2))

# Singleton instance
recognition_service = ImageRecognitionService()
