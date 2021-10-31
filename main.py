from bs4 import BeautifulSoup
import requests
import meaning
import MeaningBuilder
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('ダウンロードしたJSONファイル名.json', scope)

gc = gspread.authorize(credentials)

SPREADSHEET_KEY = 'スプレッドシートキー'

def _get_source(word):
    src = requests.get("http://ejje.weblio.jp/content/" + word)
    return src.text


def get_meaning(word):
  builder = MeaningBuilder.MeaningBuilder()
  src = _get_source(word)
  soup = BeautifulSoup(src, 'html5lib')

  # 最初に来た辞書に含まれるデータを含む行のリストを抽出する
  kiji = soup.find("div", class_='kiji')
  lines = kiji.find_all("div", class_="level0")


  for line in lines:
    # 動詞、他動詞など、タイトルを表すような行であるときの処理
    node = line.find('div', class_="KnenjSub")

    if node is not None:
      temp = ""
      sub = node.find('span', class_='KejjeSm')
      if sub is not None:
        temp = sub.get_text(strip=True)
        sub.extract()

      if temp != "":
        builder.add_part(node.get_text(strip=True))
      else:
        builder.add_tori(node.get_text(strip=True))
      continue

    # 大文字見出しが含まれる場合
    u_alph = line.find('span', class_="lvlUAH")
    if u_alph is not None:
      builder.add_u_alph(u_alph.get_text(strip=True))
      u_alph.extract()
      continue

    # 1, a などと説明を表す行の処理
    mean = line.find('p', class_="lvlB")
    number = line.find('p', class_="lvlNH")
    alph = line.find('p', class_="lvlAH")

    # 取得する順番実際の並びの反対となるため、一時的に値を保持して処理する
    mean_dat = None
    number_dat = None
    alph_dat =None

    if mean is not None:
      mean_dat = mean.get_text(strip=True)
      mean.extract()
    if alph is not None:
      if alph.get_text(strip=True) != '':
        alph_dat = alph.get_text(strip=True)
        alph.extract()
    if number is not None:
      if number.get_text(strip=True) != '':
        number_dat = number.get_text(strip=True)
        number.extract()

    if number_dat is not None:
        builder.add_number(number_dat)
    if alph_dat is not None:
        builder.add_alph(alph_dat)
    if mean_dat is not None:
        builder.add_mean(mean_dat)

    if mean is None and alph is None and number is None:
        builder.add_mean(line.get_text(strip=True))

  return builder.get_meaning()


if __name__ == "__main__":
  worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
  a_count = 1
  b_count = 1

  # 単語と意味が空白の位置を特定
  while True:
    a = str(worksheet.acell('A'+str(a_count)).value)
    print(a_count)
    if a == "None":
      break
    a_count += 1

  while True:
    b = str(worksheet.acell('B'+str(b_count)).value)
    print(b_count)
    if b == "None":
      break
    b_count += 1

  # weblioから意味をダウンロード
  for num in range(b_count, a_count):
    import_value = str(worksheet.acell('A'+str(num)).value)
    print(import_value)
    try:
      export_value = get_meaning(import_value).get_all()
    except AttributeError:
      export_value = "-"
    worksheet.update_cell(num, 2, export_value)