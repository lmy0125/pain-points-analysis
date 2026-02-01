"""
Unit tests for the Pain Points Analysis Bot
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import json
from datetime import datetime


class TestRedditExtractor(unittest.TestCase):
    """Test Reddit extraction functionality."""
    
    @patch('reddit_extractor.praw.Reddit')
    def test_extractor_initialization(self, mock_reddit):
        """Test that RedditExtractor initializes correctly."""
        from reddit_extractor import RedditExtractor
        
        extractor = RedditExtractor()
        self.assertIsNotNone(extractor.reddit)
        self.assertIsInstance(extractor.subreddits, list)
        self.assertIsInstance(extractor.max_posts, int)


class TestLLMProcessor(unittest.TestCase):
    """Test LLM processing functionality."""
    
    @patch('llm_processor.OpenAI')
    def test_processor_initialization(self, mock_openai):
        """Test that LLMProcessor initializes correctly."""
        from llm_processor import LLMProcessor
        
        processor = LLMProcessor()
        self.assertIsNotNone(processor.client)
    
    def test_categorize_empty_posts(self):
        """Test categorization with empty post list."""
        from llm_processor import LLMProcessor
        
        with patch('llm_processor.OpenAI'):
            processor = LLMProcessor()
            result = processor.categorize_posts([])
            
            self.assertIn('Problems', result)
            self.assertIn('Questions', result)
            self.assertIn('Success Stories', result)
            self.assertEqual(len(result['Problems']), 0)


class TestReportGenerator(unittest.TestCase):
    """Test report generation functionality."""
    
    @patch('report_generator.OpenAI')
    def test_generator_initialization(self, mock_openai):
        """Test that ReportGenerator initializes correctly."""
        from report_generator import ReportGenerator
        
        generator = ReportGenerator()
        self.assertIsNotNone(generator.client)
    
    @patch('report_generator.OpenAI')
    def test_generate_report_structure(self, mock_openai):
        """Test that generated report has correct structure."""
        from report_generator import ReportGenerator
        
        generator = ReportGenerator()
        
        sample_data = {
            'Problems': [
                {'title': 'Test problem', 'score': 50, 'key_issue': 'test'}
            ],
            'Questions': [],
            'Success Stories': []
        }
        
        report = generator.generate_report(sample_data)
        
        # Check report structure
        self.assertIn('generated_at', report)
        self.assertIn('summary', report)
        self.assertIn('top_5_common_hurdles', report)
        self.assertIn('categorized_posts', report)
        
        # Check summary
        self.assertIn('total_posts_analyzed', report['summary'])
        self.assertIn('problems', report['summary'])
        self.assertIn('questions', report['summary'])
        self.assertIn('success_stories', report['summary'])
    
    @patch('report_generator.OpenAI')
    def test_format_report_text(self, mock_openai):
        """Test text formatting of report."""
        from report_generator import ReportGenerator
        
        generator = ReportGenerator()
        
        sample_report = {
            'generated_at': '2024-01-15T10:00:00',
            'period': 'Last 7 days',
            'summary': {
                'total_posts_analyzed': 100,
                'problems': 50,
                'questions': 30,
                'success_stories': 20
            },
            'top_5_common_hurdles': [
                {
                    'rank': 1,
                    'title': 'Test Hurdle',
                    'description': 'Test description',
                    'frequency': '10 posts',
                    'examples': ['Example 1', 'Example 2']
                }
            ]
        }
        
        text = generator.format_report_text(sample_report)
        
        # Check that key elements are in the text
        self.assertIn('WEEKLY PAIN POINTS ANALYSIS REPORT', text)
        self.assertIn('TOP 5 COMMON HURDLES', text)
        self.assertIn('Test Hurdle', text)


class TestBot(unittest.TestCase):
    """Test main bot functionality."""
    
    @patch('bot.RedditExtractor')
    @patch('bot.LLMProcessor')
    @patch('bot.ReportGenerator')
    def test_bot_initialization(self, mock_gen, mock_proc, mock_ext):
        """Test that Bot initializes all components."""
        from bot import PainPointsBot
        
        bot = PainPointsBot()
        self.assertIsNotNone(bot.extractor)
        self.assertIsNotNone(bot.processor)
        self.assertIsNotNone(bot.generator)


if __name__ == '__main__':
    unittest.main()
