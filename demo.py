"""
Demo script with mock data to demonstrate the bot functionality
This shows how the bot works without requiring actual API credentials
"""
import json
from datetime import datetime
from report_generator import ReportGenerator


def create_mock_data():
    """Create mock categorized posts for demonstration."""
    return {
        'Problems': [
            {
                'id': '1',
                'title': 'Struggling to acquire first customers for my SaaS',
                'body': 'Launched 3 months ago, spent $5K on ads but no conversions',
                'score': 156,
                'subreddit': 'Entrepreneur',
                'permalink': 'https://reddit.com/r/Entrepreneur/example1',
                'key_issue': 'High customer acquisition cost'
            },
            {
                'id': '2',
                'title': 'Technical debt is killing my startup',
                'body': 'We built MVP quickly but now can\'t add features without breaking things',
                'score': 143,
                'subreddit': 'SaaS',
                'permalink': 'https://reddit.com/r/SaaS/example2',
                'key_issue': 'Poor code quality and architecture'
            },
            {
                'id': '3',
                'title': 'Can\'t find a technical co-founder',
                'body': 'I\'m a business person with a great idea but no one wants to join without funding',
                'score': 132,
                'subreddit': 'Entrepreneur',
                'permalink': 'https://reddit.com/r/Entrepreneur/example3',
                'key_issue': 'Team building challenges'
            },
            {
                'id': '4',
                'title': 'Burned through runway faster than expected',
                'body': 'We have 3 months of runway left and product isn\'t ready',
                'score': 128,
                'subreddit': 'SaaS',
                'permalink': 'https://reddit.com/r/SaaS/example4',
                'key_issue': 'Cash flow management'
            },
            {
                'id': '5',
                'title': 'Dealing with copycats stealing our features',
                'body': 'Larger competitor launched similar features and we\'re losing users',
                'score': 117,
                'subreddit': 'SaaS',
                'permalink': 'https://reddit.com/r/SaaS/example5',
                'key_issue': 'Competition and differentiation'
            },
            {
                'id': '6',
                'title': 'Pricing model isn\'t working',
                'body': 'Users love the product but won\'t pay our current prices',
                'score': 95,
                'subreddit': 'SaaS',
                'permalink': 'https://reddit.com/r/SaaS/example6',
                'key_issue': 'Pricing and monetization'
            },
            {
                'id': '7',
                'title': 'Scaling infrastructure costs are too high',
                'body': 'AWS bills doubled but revenue only up 20%',
                'score': 89,
                'subreddit': 'SaaS',
                'permalink': 'https://reddit.com/r/SaaS/example7',
                'key_issue': 'Technical scalability'
            },
            {
                'id': '8',
                'title': 'Customer churn is increasing',
                'body': 'Losing 15% of customers each month, can\'t figure out why',
                'score': 84,
                'subreddit': 'SaaS',
                'permalink': 'https://reddit.com/r/SaaS/example8',
                'key_issue': 'Customer retention'
            }
        ],
        'Questions': [
            {
                'id': '9',
                'title': 'What\'s the best way to validate a SaaS idea?',
                'body': 'Should I build an MVP or do customer interviews first?',
                'score': 78,
                'subreddit': 'Entrepreneur',
                'permalink': 'https://reddit.com/r/Entrepreneur/example9',
                'key_issue': 'Validation strategy'
            },
            {
                'id': '10',
                'title': 'How do you handle taxes as a solo founder?',
                'body': 'Just starting out and confused about LLC vs S-Corp',
                'score': 67,
                'subreddit': 'Entrepreneur',
                'permalink': 'https://reddit.com/r/Entrepreneur/example10',
                'key_issue': 'Legal and tax questions'
            }
        ],
        'Success Stories': [
            {
                'id': '11',
                'title': 'Hit $10K MRR after 18 months!',
                'body': 'Started with $0 marketing budget, grew through content',
                'score': 234,
                'subreddit': 'SaaS',
                'permalink': 'https://reddit.com/r/SaaS/example11',
                'key_issue': 'Revenue milestone achieved'
            },
            {
                'id': '12',
                'title': 'Finally got accepted into YC!',
                'body': 'Applied 3 times, here\'s what we learned',
                'score': 189,
                'subreddit': 'Entrepreneur',
                'permalink': 'https://reddit.com/r/Entrepreneur/example12',
                'key_issue': 'Accelerator acceptance'
            }
        ]
    }


def main():
    """Run demo with mock data."""
    print("=" * 80)
    print("PAIN POINTS ANALYSIS BOT - DEMO MODE")
    print("=" * 80)
    print("\nThis demo shows how the bot works with mock data.")
    print("To use with real data, configure your API credentials in .env\n")
    
    # Create mock data
    print("[1/3] Using mock categorized posts...")
    categorized_posts = create_mock_data()
    print(f"  - Problems: {len(categorized_posts['Problems'])}")
    print(f"  - Questions: {len(categorized_posts['Questions'])}")
    print(f"  - Success Stories: {len(categorized_posts['Success Stories'])}")
    
    # Generate report (will use fallback method without OpenAI key)
    print("\n[2/3] Generating report...")
    generator = ReportGenerator()
    
    # Override to use fallback for demo
    report = generator.generate_report(categorized_posts)
    
    # Display report
    print("\n[3/3] Report generated!\n")
    print(generator.format_report_text(report))
    
    # Save report
    filename = f"demo_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = generator.save_report(report, filename)
    print(f"\nFull report saved to: {filepath}")


if __name__ == "__main__":
    main()
