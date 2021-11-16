from flask import Flask, render_template, request, url_for
import requests
from datetime import datetime, timedelta
import json

app = Flask(__name__)

DATE = datetime.strftime((datetime.now() - timedelta(29)), '%Y-%m-%d')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/query")
def query():

    QUERY=str(request.args.get("name"))

    if QUERY == '':
        return render_template("error.html")

    else:
        address = ('https://newsapi.org/v2/everything?'
            'q='+ QUERY +
            '&from=' + DATE +
            '&sortBy=popularity&'
            'apiKey=368caa2e68b14beebcf4a2b9d2739c01')

        # register at newsapi.org/register to get your free api key

        response = requests.get(address)
        jsonResponse = response.json()

        columns = ['Source', 'Author', 'Title' , 'Description' ,
        'Url', 'Urltoimage' , 'Published At', 'Content']

        source,author,title,description,url,urltoimage,publishedat,content = ([],[],[],[],[],[],[],[])

        for item in jsonResponse['articles']:
            source.append(item['source']['name'])
            author.append(item['author'])
            title.append(item['title'])
            description.append(item['description'])
            url.append(item['url'])
            urltoimage.append(item['urlToImage'])
            publishedat.append(datetime.fromisoformat(item['publishedAt'][:-1]))
            content.append(item['content'])



        return render_template("query.html", QUERY=request.args.get("name"), source=source, author=author,
        title=title, description=description, url=url, urltoimage=urltoimage, publishedat=publishedat, content=content, columns=columns)
