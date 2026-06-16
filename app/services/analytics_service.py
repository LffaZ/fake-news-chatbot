import re
import json
from collections import Counter
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDate, ExtractHour
from app.models import UserQuery 

def get_top_keywords(text_list, top_n=10):
    """
    Extracts top keywords from a list of strings.
    Filters out common Indonesian and English stopwords, and short words.
    """
    stopwords = {
        'apakah', 'bagaimana', 'apa', 'siapa', 'kapan', 'di', 'ke', 'dari', 
        'yang', 'dan', 'atau', 'ini', 'itu', 'untuk', 'dengan', 'dalam', 'pada', 
        'bahwa', 'tentang', 'adalah', 'berita', 'hoaks', 'hoax', 'fakta', 'cek',
        'the', 'is', 'are', 'a', 'an', 'of', 'to', 'in', 'for', 'with', 'on', 'at', 
        'by', 'from', 'it', 'that', 'this', 'about'
    }
    
    words = []
    for text in text_list:
        if not text:
            continue
        # Remove punctuation and convert to lowercase
        clean_text = re.sub(r'[^\w\s]', '', text.lower())
        # Split and filter
        words.extend([w for w in clean_text.split() if w not in stopwords and len(w) > 2])
        
    return dict(Counter(words).most_common(top_n))

def get_dashboard_context():
        context = {}
        now = timezone.now()
        
        # 1. KPI Cards Variables
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=today_start.weekday())
        month_start = today_start.replace(day=1)

        total_queries = UserQuery.objects.count()
        today_queries = UserQuery.objects.filter(timestamp__gte=today_start).count()
        week_queries = UserQuery.objects.filter(timestamp__gte=week_start).count()
        month_queries = UserQuery.objects.filter(timestamp__gte=month_start).count()

        # 2. Query Trend Per Day (Last 30 Days)
        thirty_days_ago = today_start - timedelta(days=5)
        trend_qs = (
            UserQuery.objects.filter(timestamp__gte=thirty_days_ago)
            .annotate(date=TruncDate('timestamp'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )
        
        # Populate missing dates with 0 for a smooth chart
        trend_dict = {item['date'].strftime('%Y-%m-%d'): item['count'] for item in trend_qs}
        trend_labels = []
        trend_data = []
        for i in range(30, -1, -1):
            day = (today_start - timedelta(days=i)).strftime('%Y-%m-%d')
            trend_labels.append(day)
            trend_data.append(trend_dict.get(day, 0))

        # 3. Query Activity By Hour (0-23)
        hourly_qs = (
            UserQuery.objects.annotate(hour=ExtractHour('timestamp'))
            .values('hour')
            .annotate(count=Count('id'))
            .order_by('hour')
        )
        
        hourly_counts = [0] * 24
        for item in hourly_qs:
            if item['hour'] is not None:
                hourly_counts[item['hour']] = item['count']
                
        hour_labels = [f"{h:02d}:00" for h in range(24)]

        # 4. Top Keywords (Horizontal Bar)
        # Fetching all questions (optimize with .iterator() or limit to last N if DB grows large)
        all_questions = UserQuery.objects.values_list('question', flat=True).order_by('-timestamp')[:5000]
        top_keywords = get_top_keywords(all_questions, 10)
        
        keyword_labels = list(top_keywords.keys())
        keyword_data = list(top_keywords.values())

        # 5. Tables & Cards Data
        # Using select_related/prefetch_related isn't needed here as there are no foreign keys
        latest_20_queries = UserQuery.objects.order_by('-timestamp')[:20]
        recent_10_queries = latest_20_queries[:10]  # Slice the already evaluated list to save a query

        # 6. Label Distribution
        label_qs = (
            UserQuery.objects
            .values('label')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        label_labels = []
        label_data = []

        for item in label_qs:
            label_labels.append(item['label'] if item['label'] else 'unknown')
            label_data.append(item['count'])
        # Update context
        context.update({
            'kpis': {
                'total_news': 72134,
                'total_hoax': 37106,
                'total_valid': 35028,
                'total_queries': total_queries,
            },
            'trend_labels': json.dumps(trend_labels),
            'trend_data': json.dumps(trend_data),
            'hour_labels': json.dumps(hour_labels),
            'hour_data': json.dumps(hourly_counts),
            'keyword_labels': json.dumps(keyword_labels),
            'keyword_data': json.dumps(keyword_data),
            'latest_20_queries': latest_20_queries,
            'recent_10_queries': recent_10_queries,
            'label_labels': json.dumps(label_labels),
            'label_data': json.dumps(label_data),
        })
        
        return context