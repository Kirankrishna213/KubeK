
import openai
import yaml
import spacy
from typing import Dict, Any
from pathlib import Path

class NLPProcessor:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config = self._load_config(config_path)
        self.nlp = spacy.load("en_core_web_sm")
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def process_natural_language(self, user_input: str) -> Dict[str, Any]:
        # First, use spaCy for basic entity recognition
        doc = self.nlp(user_input)
        
        # Extract entities and intent
        entities = {
            "kubernetes": any(token.text.lower() in ["kubernetes", "k8s", "cluster", "pod"] for token in doc),
            "github": any(token.text.lower() in ["github", "repo", "repository", "issue"] for token in doc),
            "verbs": [token.lemma_ for token in doc if token.pos_ == "VERB"],
            "nouns": [token.lemma_ for token in doc if token.pos_ == "NOUN"]
        }
        
        # Then use OpenAI for more complex understanding
        prompt = f"""
        Analyze this Kubernetes/GitHub management request and extract:
        1. Target system (kubernetes or github)
        2. Action (get, create, delete, etc.)
        3. Target resource (pods, deployments, repositories, etc.)
        4. Any additional parameters (names, counts, filters)
        
        Return as JSON with those keys.
        
        Request: {user_input}
        """
        
        response = openai.chat.completions.create(
            model=self.config["openai"]["model"],
            messages=[{"role": "user", "content": prompt}],
            temperature=self.config["openai"]["temperature"],
            max_tokens=self.config["openai"]["max_tokens"]
        )
        
        try:
            parsed = eval(response.choices[0].message.content)
            return {**entities, **parsed}
        except:
            return entities
