import feedparser
import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict
import os

class AINewsCollector:
    """收集 AI 前沿新闻"""
    
    def __init__(self):
        self.news_list = []
        self.categories = {
            '大模型': ['GPT', 'Claude', 'LLaMA', 'Gemini', 'Mixtral', '语言模型', '大模型', 'LLM'],
            '场景动态': ['应用', '产品', '融资', '创业', '行业', '企业'],
        }
    
    def collect_from_rss(self) -> List[Dict]:
        """从 RSS 源收集新闻"""
        rss_sources = [
            {
                'url': 'https://feeds.bloomberg.com/markets/news.rss',
                'category': '场景动态'
            },
            {
                'url': 'https://feeds.techcrunch.com/techcrunch/',
                'category': '场景动态'
            },
            {
                'url': 'https://feeds.arstechnica.com/arstechnica/index',
                'category': '大模型'
            },
        ]
        
        news_items = []
        
        for source in rss_sources:
            try:
                feed = feedparser.parse(source['url'])
                for entry in feed.entries[:5]:  # 每个源取前5条
                    item = {
                        'title': entry.get('title', ''),
                        'content': entry.get('summary', '')[:200],
                        'source': entry.get('link', ''),
                        'category': source['category'],
                        'published': entry.get('published', datetime.now().isoformat()),
                        'origin': feed.feed.get('title', 'RSS Feed')
                    }
                    news_items.append(item)
            except Exception as e:
                print(f"Error fetching from {source['url']}: {e}")
        
        return news_items
    
    def collect_from_hackernews(self) -> List[Dict]:
        """从 Hacker News 收集新闻"""
        news_items = []
        try:
            response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json', timeout=10)
            top_stories = response.json()[:30]
            
            for story_id in top_stories:
                try:
                    story_response = requests.get(
                        f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json',
                        timeout=5
                    )
                    story = story_response.json()
                    
                    if story and 'title' in story:
                        # 分类判断
                        title_lower = story['title'].lower()
                        category = self._categorize_news(title_lower)
                        
                        item = {
                            'title': story['title'],
                            'content': f"讨论数: {story.get('descendants', 0)}",
                            'source': f"https://news.ycombinator.com/item?id={story_id}",
                            'category': category,
                            'published': datetime.now().isoformat(),
                            'origin': 'Hacker News'
                        }
                        news_items.append(item)
                        
                        if len(news_items) >= 20:
                            break
                except Exception as e:
                    continue
        except Exception as e:
            print(f"Error fetching from Hacker News: {e}")
        
        return news_items
    
    def _categorize_news(self, text: str) -> str:
        """根据关键词分类新闻"""
        text_lower = text.lower()
        
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    return category
        
        return '场景动态'  # 默认分类
    
    def collect_all_news(self, limit: int = 20) -> List[Dict]:
        """收集所有新闻"""
        print("开始收集 AI 新闻...")
        
        # 收集来自不同源的新闻
        all_news = []
        
        # 从 Hacker News 收集
        hackernews_items = self.collect_from_hackernews()
        all_news.extend(hackernews_items)
        
        # 从 RSS 收集
        rss_items = self.collect_from_rss()
        all_news.extend(rss_items)
        
        # 去重并限制数量
        seen_titles = set()
        unique_news = []
        
        for item in all_news:
            if item['title'] not in seen_titles:
                seen_titles.add(item['title'])
                unique_news.append(item)
                
                if len(unique_news) >= limit:
                    break
        
        # 按类别排序
        unique_news.sort(key=lambda x: (x['category'], x['published']), reverse=True)
        
        print(f"成功收集 {len(unique_news)} 条新闻")
        return unique_news


def save_news_to_json(news: List[Dict], filename: str = 'news_data.json'):
    """保存新闻到 JSON 文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(news, f, ensure_ascii=False, indent=2)
    print(f"新闻已保存到 {filename}")


if __name__ == '__main__':
    collector = AINewsCollector()
    news = collector.collect_all_news(limit=20)
    save_news_to_json(news)
