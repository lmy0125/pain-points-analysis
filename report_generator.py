"""
Report Generator Module
Synthesizes categorized posts into a weekly report with top 5 Common Hurdles.
"""
import os
import json
from typing import List, Dict
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class ReportGenerator:
    """Handles generation of weekly pain points reports."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-4o-mini"
    
    def generate_report(self, categorized_posts: Dict[str, List[Dict]]) -> Dict:
        """
        Generate a weekly report with top 5 Common Hurdles.
        
        Args:
            categorized_posts: Dictionary with categorized posts
            
        Returns:
            Dictionary containing the report
        """
        print("Generating weekly report...")
        
        # Extract problems for hurdle analysis
        problems = categorized_posts.get('Problems', [])
        
        # Generate top 5 common hurdles
        top_hurdles = self._identify_common_hurdles(problems)
        
        # Create report structure
        report = {
            'generated_at': datetime.now().isoformat(),
            'period': f"Last {os.getenv('DAYS_BACK', '7')} days",
            'summary': {
                'total_posts_analyzed': sum(len(posts) for posts in categorized_posts.values()),
                'problems': len(categorized_posts.get('Problems', [])),
                'questions': len(categorized_posts.get('Questions', [])),
                'success_stories': len(categorized_posts.get('Success Stories', []))
            },
            'top_5_common_hurdles': top_hurdles,
            'categorized_posts': {
                'Problems': self._format_posts(categorized_posts.get('Problems', [])[:10]),
                'Questions': self._format_posts(categorized_posts.get('Questions', [])[:10]),
                'Success Stories': self._format_posts(categorized_posts.get('Success Stories', [])[:10])
            }
        }
        
        print(f"Report generated with {len(top_hurdles)} hurdles identified")
        return report
    
    def _identify_common_hurdles(self, problems: List[Dict]) -> List[Dict]:
        """Use LLM to identify top 5 common hurdles from problems."""
        if not problems:
            return []
        
        # Prepare problems for analysis
        problems_text = []
        for idx, post in enumerate(problems[:50]):  # Limit to top 50 problems
            problem_text = f"{idx + 1}. {post['title']}"
            if post.get('key_issue'):
                problem_text += f" - {post['key_issue']}"
            problems_text.append(problem_text)
        
        prompt = f"""Analyze these problem posts from entrepreneur and SaaS communities.
Identify the TOP 5 COMMON HURDLES (recurring themes/pain points) that appear most frequently.

For each hurdle:
1. Give it a clear, concise title
2. Provide a brief description
3. Estimate how many posts relate to it
4. List 2-3 specific examples from the posts

Return ONLY a JSON array with this format:
[
  {{
    "rank": 1,
    "title": "Brief hurdle title",
    "description": "What this hurdle is about",
    "frequency": "estimated number of affected posts",
    "examples": ["example 1", "example 2"]
  }}
]

Problem posts:
{chr(10).join(problems_text)}"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at identifying patterns and common themes in entrepreneur and SaaS pain points."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Extract JSON from response
            if result_text.startswith('```'):
                result_text = result_text.split('```')[1]
                if result_text.startswith('json'):
                    result_text = result_text[4:]
            
            hurdles = json.loads(result_text)
            return hurdles[:5]  # Ensure only top 5
            
        except Exception as e:
            print(f"Error identifying hurdles: {e}")
            return self._fallback_hurdle_analysis(problems)
    
    def _fallback_hurdle_analysis(self, problems: List[Dict]) -> List[Dict]:
        """Simple fallback analysis if LLM fails."""
        # Basic keyword-based analysis
        keywords = {
            'customer_acquisition': ['customer', 'user', 'traffic', 'marketing', 'sales'],
            'technical': ['technical', 'bug', 'code', 'development', 'feature'],
            'funding': ['funding', 'money', 'investor', 'revenue', 'profit'],
            'team': ['team', 'hire', 'employee', 'cofounder', 'partner'],
            'product': ['product', 'feature', 'design', 'ui', 'ux']
        }
        
        counts = {key: 0 for key in keywords}
        
        for post in problems:
            text = (post['title'] + ' ' + post.get('body', '')).lower()
            for category, words in keywords.items():
                if any(word in text for word in words):
                    counts[category] += 1
        
        # Create simple hurdles list
        sorted_categories = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        hurdles = []
        for rank, (category, count) in enumerate(sorted_categories[:5], 1):
            hurdles.append({
                'rank': rank,
                'title': category.replace('_', ' ').title(),
                'description': f'Issues related to {category.replace("_", " ")}',
                'frequency': f'~{count} posts',
                'examples': []
            })
        
        return hurdles
    
    def _format_posts(self, posts: List[Dict]) -> List[Dict]:
        """Format posts for report."""
        formatted = []
        for post in posts:
            formatted.append({
                'title': post['title'],
                'subreddit': post.get('subreddit', ''),
                'score': post.get('score', 0),
                'permalink': post.get('permalink', ''),
                'key_issue': post.get('key_issue', '')
            })
        return formatted
    
    def save_report(self, report: Dict, filename: str = None):
        """Save report to a JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"report_{timestamp}.json"
        
        # Create reports directory if it doesn't exist
        os.makedirs('reports', exist_ok=True)
        filepath = os.path.join('reports', filename)
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Report saved to {filepath}")
        return filepath
    
    def format_report_text(self, report: Dict) -> str:
        """Format report as human-readable text."""
        lines = []
        lines.append("=" * 80)
        lines.append("WEEKLY PAIN POINTS ANALYSIS REPORT")
        lines.append("=" * 80)
        lines.append(f"\nGenerated: {report['generated_at']}")
        lines.append(f"Period: {report['period']}")
        lines.append(f"\nSUMMARY")
        lines.append("-" * 40)
        lines.append(f"Total posts analyzed: {report['summary']['total_posts_analyzed']}")
        lines.append(f"  - Problems: {report['summary']['problems']}")
        lines.append(f"  - Questions: {report['summary']['questions']}")
        lines.append(f"  - Success Stories: {report['summary']['success_stories']}")
        
        lines.append(f"\n\nTOP 5 COMMON HURDLES")
        lines.append("=" * 80)
        
        for hurdle in report['top_5_common_hurdles']:
            lines.append(f"\n{hurdle['rank']}. {hurdle['title']}")
            lines.append(f"   {hurdle['description']}")
            lines.append(f"   Frequency: {hurdle['frequency']}")
            if hurdle.get('examples'):
                lines.append(f"   Examples:")
                for example in hurdle['examples']:
                    lines.append(f"     - {example}")
        
        lines.append("\n" + "=" * 80)
        return '\n'.join(lines)


if __name__ == "__main__":
    # Test with sample data
    generator = ReportGenerator()
    sample_data = {
        'Problems': [
            {'title': 'Struggling with customer acquisition', 'score': 50, 'key_issue': 'CAC too high'},
            {'title': 'Technical debt is killing us', 'score': 45, 'key_issue': 'Legacy code'}
        ],
        'Questions': [],
        'Success Stories': []
    }
    report = generator.generate_report(sample_data)
    print(generator.format_report_text(report))
