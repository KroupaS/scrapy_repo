from flats500.flats500.spiders.flats500 import Flats500Spider
from scrapy.crawler import CrawlerProcess

from http.server import HTTPServer, BaseHTTPRequestHandler
import psycopg2

def build_html(output_name):
    conn = psycopg2.connect(dbname="postgres_database", user="postgres", password="heslo123", host="postgres_db", port="5432")
    cur = conn.cursor()
    cur.execute("SELECT * FROM flats")
    all_flats = cur.fetchall()

    output_html = open(output_name, 'w', encoding="utf-8")
    output_html.write("<!DOCTYPE html><html><head>")
    output_html.write("<title>500 flats for sale</title>")
    output_html.write("<style>")
    output_html.write("h1{color:black; text-align:center;}img{vertical-align:middle;}.centered{text-align:center;}")
    output_html.write(".centered span{width: 300px; display:inline-block; text-align:left; line-height:150%}")
    output_html.write(".centered ul {display:inline-block; margin:0; padding:0; list-style:none;}.centered li {float: left; padding: 2px 5px;}")
    output_html.write("</style>")
    output_html.write("</head><body>")
    output_html.write("<h1>500 flats for sale</h1><div class=\"centered\"><ul>")
    for i in range(len(all_flats)):
        item_string = "<li><span>"
        item_string += "<b>" +  all_flats[i][1] + "</b>" + "<br>" + all_flats[i][2]
        item_string += "</span>"
        item_string += "<img src=" + all_flats[i][3] + ">"
        item_string += "</li><br>"
        output_html.write(item_string)
    output_html.write("</div></ul></body></html>")
    print("HTML file built")


class FlatsHTTP(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        print("GET RESPONSE", flush = True)

        f = open('./index.html', encoding="utf-8")
        for line in f:
            self.wfile.write(bytes(line, "utf-8"))


process = CrawlerProcess(settings = {
    'ITEM_PIPELINES' : {'flats500.flats500.pipelines.FlatsPipeline' : 500,},
    })

process.crawl(Flats500Spider)
process.start()

build_html("index.html")
server = HTTPServer(("0.0.0.0", 8080), FlatsHTTP)
print("Server running", flush = True)
server.serve_forever()
server.server_close()
print("Server stopped")
