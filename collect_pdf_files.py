import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import os

def extract_pdf_links_from_html(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    pdf_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.lower().endswith('.pdf'):
            text = link.get_text(strip=True)
            full_url = urljoin(base_url, href)
            pdf_links.append((text, full_url))
    return pdf_links

def extract_pdf_links_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    html_content = response.text
    return extract_pdf_links_from_html(html_content, url)

def save_links_to_csv(links, csv_file_path):
    df = pd.DataFrame(links, columns=['Text', 'URL'])
    df.to_csv(csv_file_path, index=False, encoding='utf-16', sep='\t')
    
def download_pdf(pdf_url, save_folder):
    response = requests.get(pdf_url)
    response.raise_for_status()
    filename = os.path.basename(pdf_url)
    file_path = os.path.join(save_folder, filename)
    with open(file_path, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {pdf_url} to {file_path}")

# ダウンロード先のフォルダパス
save_folder = r"C:\Users\81802\OneDrive\デスクトップ\研究室AIチャットbot\リンク情報"

# URLからPDFリンクを抽出
url = 'https://www.seikei.ac.jp/university/education/webkisokushu/hosyounin.html'
pdf_links = extract_pdf_links_from_url(url)
print("Extracted PDF links:")
for text, link_url in pdf_links:
    print(f"Text: {text}, URL: {link_url}")

# ディレクトリがない場合生成
os.makedirs(save_folder, exist_ok=True)

# CSVファイルに保存するパス
csv_file_path = os.path.join(save_folder, 'PDFリンク情報.csv')

# PDFリンク情報をCSVファイルに保存
save_links_to_csv(pdf_links, csv_file_path)
print(f"Saved PDF links to {csv_file_path}")

for text, pdf_url in pdf_links:
    download_pdf(pdf_url, save_folder)
