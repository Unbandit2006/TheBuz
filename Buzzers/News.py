import gnews

def get_news():
    news = gnews.GNews(max_results=5)
    
    string = ""
    for x in news.get_top_news():
        title = x["title"]
        string += f"{title}\n\n"

    return string

