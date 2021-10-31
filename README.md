# スプレッドシートに入力した英単語を自動で意味を出力するプログラム
表題通り
スプレッドシートに入力した英単語をweblioの辞書を利用して意味を自動で出力する
『Anki』などのアプリケーションと組み合わせると効力を発揮する

## 動作に必要なもの
 * python ver3.8
 * requests (pip install requests)
 * BeautifulSoup4 (pip install beautifulsoup4)
 * html5lib (pip install html5lib)

## 使用方法
1. このサイト[1]の手順通り,Google Cloud Platform からAPIを用意する
2. main.py の11,15行目を自身のものへ変更する
3. A列に単語を入力し，このプログラムを実行するとB列に出力される

## 参考文献
[1]https://tanuhack.com/operate-spreadsheet/
[2]https://github.com/Uehara25/WeblioSearcher