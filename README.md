# Pain Points Analysis Bot

A Reddit post summarizer that automatically extracts, categorizes, and analyzes pain points from entrepreneur and SaaS communities.

## Features

- **Extraction**: Pulls top 50-100 posts from specified subreddits every 24 hours
- **Processing**: Uses LLM (OpenAI GPT-4) to categorize posts into:
  - Problems
  - Questions
  - Success Stories
- **Synthesis**: Generates weekly reports identifying the top 5 Common Hurdles

## Setup

### Prerequisites

- Python 3.8+
- Reddit API credentials
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/lmy0125/pain-points-analysis.git
cd pain-points-analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add your credentials:
```
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=PainPointsAnalyzer/1.0
OPENAI_API_KEY=your_openai_api_key_here
SUBREDDITS=Entrepreneur,SaaS
MAX_POSTS=100
DAYS_BACK=7
```

### Getting Reddit API Credentials

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Choose "script" as the app type
4. Fill in the required fields
5. Copy the client ID and secret

## Usage

### Quick Demo (No API Keys Required)

Run the demo with mock data to see how the bot works:

```bash
python demo.py
```

This will generate a sample report using mock Reddit posts.

### Run Once (for testing)

```bash
python bot.py --once
```

### Run as Scheduled Service (24-hour intervals)

```bash
python bot.py
```

The bot will:
1. Run an analysis immediately upon startup
2. Schedule subsequent runs every 24 hours
3. Save reports to the `reports/` directory

### Output

Reports are saved as JSON files in the `reports/` directory with timestamps:
- `report_YYYYMMDD_HHMMSS.json`

Each report contains:
- Summary statistics
- Top 5 Common Hurdles with descriptions and examples
- Sample posts from each category

## Project Structure

```
pain-points-analysis/
├── bot.py                  # Main orchestration script
├── reddit_extractor.py     # Reddit API extraction module
├── llm_processor.py        # LLM categorization module
├── report_generator.py     # Report synthesis module
├── demo.py                 # Demo script with mock data
├── test_bot.py             # Unit tests
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
└── reports/              # Generated reports (created automatically)
```

## Example Report

```
================================================================================
WEEKLY PAIN POINTS ANALYSIS REPORT
================================================================================

Generated: 2024-01-15T10:30:00
Period: Last 7 days

SUMMARY
----------------------------------------
Total posts analyzed: 85
  - Problems: 45
  - Questions: 30
  - Success Stories: 10


TOP 5 COMMON HURDLES
================================================================================

1. Customer Acquisition Challenges
   Difficulty in acquiring first customers and scaling user growth
   Frequency: ~15 posts
   Examples:
     - High customer acquisition costs
     - Lack of product-market fit
     - Marketing strategy unclear

2. Technical Debt and Scalability
   Technical challenges affecting product development
   Frequency: ~12 posts
   ...
```

## Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `REDDIT_CLIENT_ID` | - | Reddit API client ID |
| `REDDIT_CLIENT_SECRET` | - | Reddit API client secret |
| `REDDIT_USER_AGENT` | PainPointsAnalyzer/1.0 | User agent string |
| `SUBREDDITS` | Entrepreneur,SaaS | Comma-separated subreddit list |
| `MAX_POSTS` | 100 | Maximum posts to analyze |
| `DAYS_BACK` | 7 | Number of days to look back |
| `OPENAI_API_KEY` | - | OpenAI API key |

## Testing

Run the test suite:

```bash
python -m unittest test_bot.py -v
```

## How It Works

1. **Extraction Phase**: 
   - Connects to Reddit API using PRAW library
   - Fetches top posts from configured subreddits
   - Filters posts from the last N days
   - Sorts by score and limits to MAX_POSTS

2. **Processing Phase**:
   - Sends post batches to OpenAI GPT-4
   - LLM categorizes each post as Problem, Question, or Success Story
   - Extracts key issues from each post
   - Falls back to keyword-based categorization if LLM fails

3. **Synthesis Phase**:
   - Analyzes all problems to identify common patterns
   - Uses LLM to synthesize top 5 recurring hurdles
   - Generates structured report with statistics
   - Saves report as JSON and formats as readable text

## License

MIT
