"""
Reddit Extractor Module
Extracts top posts from specified subreddits using the Reddit API.
"""
import praw
import os
from datetime import datetime, timedelta
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()


class RedditExtractor:
    """Handles extraction of posts from Reddit."""
    
    def __init__(self):
        """Initialize Reddit API client."""
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT', 'PainPointsAnalyzer/1.0')
        )
        self.subreddits = os.getenv('SUBREDDITS', 'Entrepreneur,SaaS').split(',')
        self.max_posts = int(os.getenv('MAX_POSTS', '100'))
        self.days_back = int(os.getenv('DAYS_BACK', '7'))
    
    def extract_posts(self) -> List[Dict]:
        """
        Extract top posts from configured subreddits.
        
        Returns:
            List of dictionaries containing post data
        """
        all_posts = []
        cutoff_date = datetime.now() - timedelta(days=self.days_back)
        
        for subreddit_name in self.subreddits:
            subreddit_name = subreddit_name.strip()
            print(f"Extracting posts from r/{subreddit_name}...")
            
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                
                # Fetch top posts from the past week
                for post in subreddit.top(time_filter='week', limit=self.max_posts):
                    post_date = datetime.fromtimestamp(post.created_utc)
                    
                    # Only include posts within the time window
                    if post_date >= cutoff_date:
                        post_data = {
                            'id': post.id,
                            'subreddit': subreddit_name,
                            'title': post.title,
                            'body': post.selftext,
                            'score': post.score,
                            'num_comments': post.num_comments,
                            'created_utc': post.created_utc,
                            'url': post.url,
                            'permalink': f"https://reddit.com{post.permalink}"
                        }
                        all_posts.append(post_data)
                
                print(f"Extracted {len([p for p in all_posts if p['subreddit'] == subreddit_name])} posts from r/{subreddit_name}")
                
            except Exception as e:
                print(f"Error extracting from r/{subreddit_name}: {e}")
        
        # Sort by score (descending) and limit to max_posts
        all_posts.sort(key=lambda x: x['score'], reverse=True)
        all_posts = all_posts[:self.max_posts]
        
        print(f"Total posts extracted: {len(all_posts)}")
        return all_posts


if __name__ == "__main__":
    extractor = RedditExtractor()
    posts = extractor.extract_posts()
    print(f"\nSample post: {posts[0] if posts else 'No posts found'}")
