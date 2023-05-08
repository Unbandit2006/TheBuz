import gnews

def get_news():
    news = gnews.GNews(max_results=5)
    
    string = "<br>Top Headlines<br>-------------<br><br>"
    for x in news.get_top_news():
        title = x["title"]
        string += f"{title}<br><br>"

    return string

