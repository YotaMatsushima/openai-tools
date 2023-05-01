from dotenv import load_dotenv
import praw
import os
import sys

# .env ファイルから環境変数をロード
load_dotenv()

# Redditアプリケーションの認証情報を設定
reddit = praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    user_agent=os.getenv('USER_AGENT'),

)

# コマンドライン引数から検索ワードを取得
query = sys.argv[1] if len(sys.argv) > 1 else "AI"

# Reddit全体から評価の高い投稿を検索
results = reddit.subreddit('all').search(query, sort='relevance', time_filter='all', limit=100)

# 結果を評価順にソートし、上位20個を取得
top_20_posts = sorted(results, key=lambda post: post.score, reverse=True)[:20]

# 各投稿のタイトル、URL、およびIDを表示
for post in top_20_posts:
    print(f'Title: {post.title}, URL: https://reddit.com{post.permalink}, Score: {post.score}, ID: {post.id}')
