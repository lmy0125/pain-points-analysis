"""
LLM Processor Module
Processes Reddit posts using an LLM to categorize them.
"""
import os
import json
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class LLMProcessor:
    """Handles LLM processing of Reddit posts."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-4o-mini"
    
    def categorize_posts(self, posts: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Categorize posts into Problems, Questions, or Success Stories.
        
        Args:
            posts: List of post dictionaries
            
        Returns:
            Dictionary with categorized posts
        """
        categorized = {
            'Problems': [],
            'Questions': [],
            'Success Stories': []
        }
        
        print(f"Categorizing {len(posts)} posts...")
        
        # Process in batches to avoid token limits
        batch_size = 5
        for i in range(0, len(posts), batch_size):
            batch = posts[i:i+batch_size]
            self._process_batch(batch, categorized)
        
        print(f"Categorization complete:")
        print(f"  Problems: {len(categorized['Problems'])}")
        print(f"  Questions: {len(categorized['Questions'])}")
        print(f"  Success Stories: {len(categorized['Success Stories'])}")
        
        return categorized
    
    def _process_batch(self, batch: List[Dict], categorized: Dict[str, List[Dict]]):
        """Process a batch of posts."""
        # Prepare posts for LLM
        posts_text = []
        for idx, post in enumerate(batch):
            post_text = f"Post {idx + 1}:\nTitle: {post['title']}\nBody: {post['body'][:500]}"
            posts_text.append(post_text)
        
        prompt = f"""Analyze the following Reddit posts from entrepreneur and SaaS communities. 
For each post, categorize it as one of:
1. "Problem" - User is describing a challenge, pain point, or issue they're facing
2. "Question" - User is asking for advice, recommendations, or information
3. "Success Story" - User is sharing an achievement, milestone, or positive outcome

Return ONLY a JSON array with the format: [{{"post_number": 1, "category": "Problem", "key_issue": "brief description"}}, ...]

Posts:
{chr(10).join(posts_text)}"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing social media posts to identify pain points, questions, and success stories in entrepreneurship and SaaS communities."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Extract JSON from response (handle markdown code blocks)
            if result_text.startswith('```'):
                result_text = result_text.split('```')[1]
                if result_text.startswith('json'):
                    result_text = result_text[4:]
            
            results = json.loads(result_text)
            
            # Map results back to posts
            for result in results:
                post_idx = result['post_number'] - 1
                if 0 <= post_idx < len(batch):
                    post = batch[post_idx].copy()
                    post['key_issue'] = result.get('key_issue', '')
                    category = result['category']
                    
                    if category == 'Problem':
                        categorized['Problems'].append(post)
                    elif category == 'Question':
                        categorized['Questions'].append(post)
                    elif category == 'Success Story':
                        categorized['Success Stories'].append(post)
                        
        except Exception as e:
            print(f"Error processing batch: {e}")
            # Fallback: categorize by basic heuristics
            for post in batch:
                title_lower = post['title'].lower()
                if any(word in title_lower for word in ['problem', 'issue', 'struggling', 'difficult', 'challenge']):
                    categorized['Problems'].append(post)
                elif '?' in post['title']:
                    categorized['Questions'].append(post)
                elif any(word in title_lower for word in ['success', 'achieved', 'milestone', 'revenue', 'growth']):
                    categorized['Success Stories'].append(post)
                else:
                    categorized['Questions'].append(post)  # Default to questions


if __name__ == "__main__":
    # Test with sample data
    processor = LLMProcessor()
    sample_posts = [
        {
            'id': '1',
            'title': 'Struggling to get my first customer',
            'body': 'I launched my SaaS 3 months ago but still no customers',
            'score': 45
        }
    ]
    result = processor.categorize_posts(sample_posts)
    print(f"\nResult: {result}")
