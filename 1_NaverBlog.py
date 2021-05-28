import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import quote

# urllib.parse.quote()는 아스키코드 형식이 아닌 글자를 URL 인코딩 시켜줍니다.

#iframe 제거 후 blog.naver.com 붙이기
def delete_iframe(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status() # 문제시 프로그램 종료
    soup = BeautifulSoup(res.text, "lxml") 

    src_url = "https://blog.naver.com/" + soup.iframe["src"]
    
    return src_url

# 네이버블로그 본문 스크래핑
def text_scraping(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status() # 문제시 프로그램 종료
    soup = BeautifulSoup(res.text, "lxml") 

    if soup.find("div", attrs={"class":"se-main-container"}):
        text = soup.find("div", attrs={"class":"se-main-container"}).get_text()
        text = text.replace("\n","") #공백 제거
        return text

    elif soup.find("div", attrs={"id":"postViewArea"}):
        text = soup.find("div", attrs={"id":"postViewArea"}).get_text()
        text = text.replace("\n","") 
        return text
    else:
        return "네이버 블로그는 맞지만, 확인불가"


query = "sk하이닉스"

url = "https://search.naver.com/search.naver?where=view&sm=tab_jum&query=" + quote(query)

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
res = requests.get(url, headers=headers)
res.raise_for_status() # 문제시 프로그램 종료
soup = BeautifulSoup(res.text, "lxml") 

posts = soup.find_all("li", attrs={"class":"bx _svp_item"})

for post in posts:
    print("-"*50)
    post_title = post.find("a", attrs={"class":"api_txt_lines total_tit"}).get_text()
    print("제목 :",post_title)
    post_link = post.find("a", attrs={"class":"api_txt_lines total_tit"})['href']
    print("link :", post_link)
    

    blog_p = re.compile("blog.naver.com")
    blog_m = blog_p.search(post_link)

    if blog_m:
        blog_text = text_scraping(delete_iframe(post_link))
        print(blog_text)
        
    else:
        print("카페 및 포스트로 인한 확인 불가")

    print("-"*50)