import logging

logger = logging.getLogger(__name__)

class NewsAnalyzer:
    def __init__(self):
        self.positive_keywords = ['상승', '계약', '호재']
        self.negative_keywords = ['하락', '악재', '우려']

    def analyze_news_sentiment(self, code, company_name):
        try:
            news_data = self.get_recent_news(company_name)
            pos, neg = 0, 0
            for news in news_data:
                text = news.get('title', '') + news.get('content', '')
                pos += sum(1 for k in self.positive_keywords if k in text)
                neg += sum(1 for k in self.negative_keywords if k in text)
            total = pos + neg
            score = (pos - neg) / total if total else 0
            return {
                'sentiment_score': score,
                'positive_count': pos,
                'negative_count': neg,
                'news_count': len(news_data)
            }
        except Exception as e:
            logger.error(f"뉴스 분석 오류 {code}: {e}")
            return {'sentiment_score': 0}

    def get_recent_news(self, company_name):
        return []
