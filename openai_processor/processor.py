import json
import openai
import os

class OpenAIProcessor:
    def __init__(self):
        # Initialize OpenAI client with API key from environment
        self.client = openai.OpenAI(base_url=os.getenv('OPENAI_API_BASE'), api_key=os.getenv('OPENAI_API_KEY'))
    
    def process_data(self):
        """
        Process the scraped data using OpenAI's API.
        Modify this method according to your specific ML needs.
        """
        # Load the scraped data
        with open('scraped_data.json', 'r') as f:
            data = json.load(f)

        # Example: Use OpenAI to analyze the content
        analysis_results = self._analyze_content(data['content'])        
        # Save the analysis results
        with open('analysis_results.json', 'w') as f:
            json.dump({
                'original_data': data,
                'analysis': analysis_results
            }, f, indent=4)


    def _analyze_content(self, content):
        """
        Helper method to analyze content using OpenAI API
        Args:
            content: Text content to analyze
        Returns:
            Text of Analysis
        """
        if not content:
            raise ValueError("Content cannot be empty")
        if not isinstance(content, str):
            raise TypeError("Content must be a string")
        if len(content) > 4*7500:
            raise ValueError("Content exceeds maximum length")
        response = self.client.chat.completions.create(
            model=os.getenv('MODEL'), 
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes text."},
                {"role": "user", "content": f"Analyze this content: {content}"}
            ]
        )
        return response.choices[0].message.content