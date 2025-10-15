from bs4 import BeautifulSoup
import requests

response = requests.get("https://www.empireonline.com/movies/features/best-movies-2/")
web_page = response.text

web = BeautifulSoup(web_page, "html.parser")
spans = web.find_all(name="span", class_="content_content__i0P3p", attrs={"data-test": "content"})

list_movies = []

for span in spans:
    h2_tag=span.find("h2")
    if h2_tag:
        strong_tag = h2_tag.find("strong")
        if strong_tag:
            list_movies.append(strong_tag.getText().strip())
print(list_movies)

with open(file="movies.txt", mode="w") as file:
    for movie in list_movies[::-1]:
        file.write(movie + "\n")