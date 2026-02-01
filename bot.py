"""
Pain Points Analysis Bot
Main script that orchestrates Reddit post extraction, LLM processing, and report generation.
Runs on a 24-hour schedule.
"""
import os
import schedule
import time
from datetime import datetime
from reddit_extractor import RedditExtractor
from llm_processor import LLMProcessor
from report_generator import ReportGenerator
from dotenv import load_dotenv

load_dotenv()


class PainPointsBot:
    """Main bot that orchestrates the pain points analysis pipeline."""
    
    def __init__(self):
        """Initialize all components."""
        self.extractor = RedditExtractor()
        self.processor = LLMProcessor()
        self.generator = ReportGenerator()
    
    def run_analysis(self):
        """Run the complete analysis pipeline."""
        print("\n" + "=" * 80)
        print(f"Starting Pain Points Analysis - {datetime.now()}")
        print("=" * 80)
        
        try:
            # Step 1: Extract posts from Reddit
            print("\n[1/3] EXTRACTION: Pulling top posts from Reddit...")
            posts = self.extractor.extract_posts()
            
            if not posts:
                print("No posts found. Skipping analysis.")
                return
            
            # Step 2: Process posts with LLM
            print("\n[2/3] PROCESSING: Categorizing posts with LLM...")
            categorized_posts = self.processor.categorize_posts(posts)
            
            # Step 3: Generate report
            print("\n[3/3] SYNTHESIS: Generating weekly report...")
            report = self.generator.generate_report(categorized_posts)
            
            # Save report
            filepath = self.generator.save_report(report)
            
            # Print report summary
            print("\n" + self.generator.format_report_text(report))
            
            print(f"\nAnalysis complete! Report saved to: {filepath}")
            
        except Exception as e:
            print(f"\nError during analysis: {e}")
            import traceback
            traceback.print_exc()
    
    def start_scheduler(self):
        """Start the 24-hour scheduled execution."""
        print("Pain Points Analysis Bot Started")
        print("=" * 80)
        print("Schedule: Running every 24 hours")
        print("Next run: Now (immediate first run)")
        print("Press Ctrl+C to stop")
        print("=" * 80)
        
        # Run immediately on startup
        self.run_analysis()
        
        # Schedule to run every 24 hours
        schedule.every(24).hours.do(self.run_analysis)
        
        # Keep the bot running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute


def main():
    """Main entry point."""
    import sys
    
    bot = PainPointsBot()
    
    # Check if we should run once or as a scheduled service
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        print("Running analysis once (no scheduling)...")
        bot.run_analysis()
    else:
        bot.start_scheduler()


if __name__ == "__main__":
    main()
