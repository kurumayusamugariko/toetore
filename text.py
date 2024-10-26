import json

data = {
    "id": ["文", "問題", "単語", "和訳"],
    "1": ["Let's try anyway.", "Let's try ______.", "anyway", "とにかくやってみよう"],
		"2": ["Following the speech, we had dinner.", "_________ the speech, we had dinner.", "following", "スピーチに続いて、夕食をとった"],
		"3": ["Please refer to the map.", "Please _______ to the map.", "refer", "地図を参照してください"],
		"4": ["Ticket are available online.", "Tickets are _______ online.", "available", "チケットはオンラインで入手可能です"],
		"5": ["the sales department.", "the _______ department.", "sales", "営業部"],
		"6": ["Thank you for your assistance", "Thank you for your ________.", "assistance", "ご協力ありがとうございます"],
		"7": ["Limited express supernatural ghosts and vengeful spirits", "Limited express ________.", "supernatural ghosts and vengeful spirits", "特急過呪怨霊"],
}

# データをファイルに保存用
with open('anyway.txt', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

# ファイルからデータを読み込む用
with open('anyway.txt', 'r', encoding='utf-8') as file:
    loaded_data = json.load(file)

print(loaded_data)