
from bs4 import  BeautifulSoup
from services.codeforces.utils import fetch_url
from models.userInfo import CodeforceUserInfo


async def get_user_info(handle: str):
    url = f"https://codeforces.com/profile/{handle}"
    html = await fetch_url(url)
    soup = BeautifulSoup(html, "html.parser")
    name= soup.select("h1 a.rated-user.user-gray")[0].text.strip()
    rating = soup.select("li span.user-gray")
    current_rating = rating[0].text.strip()
    status= rating[1].text.strip()
    max_rating = rating[2].text.strip()
    userInfo = CodeforceUserInfo(handle=name,rating=int(current_rating), maxRating=int(max_rating), status=status)
    print(userInfo)
    return userInfo









