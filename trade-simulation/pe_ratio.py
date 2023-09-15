from bs4 import BeautifulSoup
from datetime import datetime
import requests


def retrieve_pe_ratios() -> list[tuple[float, str]]:
    pe_page = requests.get("https://www.multpl.com/s-p-500-pe-ratio/table/by-month")
    soup = BeautifulSoup(pe_page.content, "html.parser")
    datatable = soup.find(id="datatable")
    rows = datatable.find_all("tr")[2:]
    pe_history = []
    for month in rows:
        cols = month.find_all("td")
        try:
            date = datetime.strptime(cols[0].text, "%b %d, %Y").timestamp()
            pe = cols[1].text.splitlines()[0]
            pe_history.append((date, pe))
        except:
            break
    pe_history.reverse()
    return pe_history
