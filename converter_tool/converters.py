import re


def ojisan_converter(text):
    """
    おじさん構文に合わせて文字列を変換する関数
    - 敬語をタメ口に変換
    - 通常のタメ口もおじさんらしくする
    - 文章が短い場合は盛る
    - 単語ごとに感情絵文字を挿入
    - 文章全体の感情を分析して文末に絵文字を付与
    例: 「やっほー○○ちゃん！君とのデート楽しい😘本当に最高だネ。毎日君のことばっかり考えてるヨ😍」
    """
    # 一人称をおじさん風に
    ojisan_pronoun_map = {
        "私は": "オレは",
        "私を": "オレを",
        "私の": "オレの",
        "僕は": "オレは",
        "僕を": "オレを",
        "僕の": "オレの",
        "わたしは": "オレは",
        "わたしを": "オレを",
        "わたしの": "オレの",
    }

    for pronoun, ojisan_pronoun in ojisan_pronoun_map.items():
        text = text.replace(pronoun, ojisan_pronoun)

    # 敬語をタメ口に変換（長い順でソート）
    polite_to_casual_map = {
        "いかがですか": "どうカナ",
        "ございます": "な",
        "させていただ": "させてもら",
        "いたします": "そうするヨ",
        "いただけますか": "もらえるカナ？",
        "いただけます": "もらえるヨ",
        "いただき": "もらい",
        "おります": "いるヨ",
        "います": "いるヨ",
        "ました": "ったネ",
        "ますか": "かなカナ？",
        "ます": "ますヨ",
        "です。": "だヨ。",
        "ですか": "かなカナ？",
        "ですね": "だネ",
        "の話": "の話さ",
        "ありがとうございます": "ありがとネ",
        "こちらこそ": "こっちこそ",
        "そうですね": "そうだヨネ",
        "そうです": "そうだヨ",
        "いいです": "いいネ",
        "良いです": "良いネ",
        "大丈夫です": "大丈夫だヨ",
        "わかりました": "わかったヨ",
        "了解です": "了解ですヨ",
    }

    # 長い順でソート
    sorted_polite = sorted(polite_to_casual_map.items(),
                           key=lambda x: len(x[0]), reverse=True)
    for polite, casual in sorted_polite:
        text = text.replace(polite, casual)

    # 通常のタメ口もおじさん構文に変換（敬語ではない普通の文も対応）
    casual_to_ojisan_map = {
        "だね。": "だネ。",
        "だね": "だネ",
        "だよ。": "だヨ。",
        "だよ": "だヨ",
        "だろう。": "だろうネ。",
        "だろう": "だろうネ",
        "である。": "だヨ。",
        "である": "だヨ",
        "いいね。": "いいネ。",
        "いいね": "いいネ",
        "いいよ。": "いいヨ。",
        "いいよ": "いいヨ",
        "そうだね。": "そうだネ。",
        "そうだね": "そうだネ",
        "そうだよ。": "そうだヨ。",
        "そうだよ": "そうだヨ",
        "ないね。": "ないネ。",
        "ないね": "ないネ",
        "ないよ。": "ないヨ。",
        "ないよ": "ないヨ",
        "ある。": "あるヨ。",
        "ある": "あるヨ",
        "できる。": "できるヨ。",
        "できる": "できるヨ",
        "思う。": "思うヨ。",
        "思う": "思うヨ",
        "ますよね？": "だろうネ？",
        "ますよね": "だろうネ",
        "ですよね？": "そうなのカナ？",
        "ですよね": "そうなのカナ",
        "です。": "だヨ。",
        "ですか": "かなカナ",
        "ですね": "だネ",
        "です": "だヨ",
    }

    sorted_casual = sorted(casual_to_ojisan_map.items(),
                           key=lambda x: len(x[0]), reverse=True)
    for casual, ojisan in sorted_casual:
        text = text.replace(casual, ojisan)

    # 助詞の古めかしい変換処理
    particle_map = {
        "ては": "ちゃあ",
        "ながら": "ながらネ",
        "しながら": "しながらヨ",
        "ね。": "ネ。",
        "ねえ": "ネエ",
        "よ。": "ヨ。",
        "よ、": "ヨ、",
        "ねえ。": "ネエ。",
        "ねえよ": "ネエヨ",
        "な。": "ナ。",
        "なあ": "ナア",
        "ぞ。": "ゾ。",
    }

    for particle, replacement in particle_map.items():
        text = text.replace(particle, replacement)

    # 句点の処理：。で終わる文に「ヨ」「ネ」を付加、および各文に感情絵文字を追加
    sentences = text.split('。')
    ojisan_sentences = []

    # 感情キーワードの定義（各文の分析用）
    positive_keywords_for_analysis = [
        '楽', '楽しみ', '嬉しい', '好き', '大好き', '愛', '幸せ', '最高', '素敵', 'デート', '会いたい', 'キス', '最強', '完璧']
    negative_keywords_for_analysis = [
        '悲', '辛い', '困った', '寂', '怒', '泣く', '嫌', '最悪', 'つらい', '嫌い']

    for i, sentence in enumerate(sentences):
        if sentence.strip():  # 空の文は無視
            sentence = sentence.strip()

            # 各文の感情を判定（表情絵文字用）
            sentence_positive_count = sum(
                1 for word in positive_keywords_for_analysis if word in sentence)
            sentence_negative_count = sum(
                1 for word in negative_keywords_for_analysis if word in sentence)

            # 既に助詞で終わっていない場合
            if not sentence.endswith(('ヨ', 'ネ', 'ナ', 'カナ', '？', 'な', 'ナ', 'ゾ', 'ネエ', 'ナア')):
                # 確認文や質問文の場合
                if '？' in sentence or sentence.endswith('か'):
                    if not sentence.endswith('？'):
                        sentence = sentence.rstrip('か').strip() + 'カナ？'
                # 通常の文
                elif i % 3 == 0:
                    sentence += 'ヨ'
                elif i % 3 == 1:
                    sentence += 'ネ'
                else:
                    sentence += 'ネ'

            # 各文の末尾に表情絵文字を追加
            emotion_emoji = ""
            if sentence_positive_count > sentence_negative_count:
                # ポジティブな感情が優位
                if '好き' in sentence or 'デート' in sentence or '愛' in sentence or '会いたい' in sentence:
                    emotion_emoji = "💕"
                elif '楽しい' in sentence or '楽しみ' in sentence:
                    emotion_emoji = "😘"
                elif '最高' in sentence or '完璧' in sentence or '最強' in sentence:
                    emotion_emoji = "😍"
                else:
                    emotion_emoji = "😊"
            elif sentence_negative_count > 0:
                # ネガティブな感情がある場合
                if '悲しい' in sentence or '泣く' in sentence or '寂しい' in sentence:
                    emotion_emoji = ['😢','😭','🥶''😭', '😥', '😓', '😰', '😨', '😱', '💧']
                elif '怒り' in sentence:
                    emotion_emoji = ['😠','😤'💢', '😡', '💥'']
                else:
                    emotion_emoji = "😭"
            else:
                # 中立的な文（ニュートラル感情にも絵文字を付与）
                if '？' in sentence:
                    # 質問文には複数パターン
                    question_emojis = ['🤔, '❓', '🙄', '😐']
                    emotion_emoji = question_emojis[i % len(question_emojis)]
                elif 'かな' in sentence or 'ようだ' in sentence or 'みたい' in sentence:
                    # 推測・推量表現
                    emotion_emoji = "🤔"
                elif 'ある' in sentence or 'いる' in sentence or 'できる' in sentence or 'なる' in sentence:
                    # 状態・存在表現
                    emotion_emoji = "😐"
                else:
                    # その他のニュートラル文
                    neutral_emojis = ['😊', '👍', '🫡', '💭', '🙂']
                    emotion_emoji = neutral_emojis[i % len(neutral_emojis)]
            
            # 既に感情絵文字が含まれていない場合のみ追加
            if sentence and not sentence.endswith(('😊', '😍', '😘', '💕', '😢', '😠', '😭', '🤔', '😲', '😂')):
                sentence += emotion_emoji
            
            ojisan_sentences.append(sentence)
    
    text = '。'.join(ojisan_sentences)
    if text and not text.endswith('。'):
        text += '。'
    
    # 別の句点パターンも処理（、で区切られた部分）
    if '、' in text:
        parts = text.split('、')
        ojisan_parts = []
        for i, part in enumerate(parts):
            if part.strip() and not part.endswith(('ヨ', 'ネ', 'ナ', 'カナ', 'ゾ', 'ネエ', 'ナア')):
                if i % 2 == 0:
                    part = part + 'ヨ'
                else:
                    part = part + 'ネ'
            ojisan_parts.append(part)
        text = '、'.join(ojisan_parts)
    
    # おじさん特有の言い回しを追加・強化
    ojisan_additions = [
        "ほんとにな、",
        "君とはなあ、",
        "最近さあ、",
        "実はさ、",
        "まじでな、",
        "ところでな、",
        "そもそもさ、",
        "ぶっちゃけな、",
        "てかね、",
    ]
    
    # 文章が短い場合は盛る
    if len(text) < 80:
        addition = ojisan_additions[len(text) % len(ojisan_additions)]
        text = addition + text
    location_emoji_map = {
        "ホテル": "🏨",
        "駅": "🚉",
        "喫茶店": "☕",
        "レストラン": "🍽️",
        "居酒屋": "🍺",
        "映画": "🎬",
        "公園": "🌳",
        "海": "🌊",
        "山": "⛰️",
    }
    
    # 食べ物・飲み物に対応する絵文字
    food_emoji_map = {
        "ラーメン": "🍜",
        "ご飯": "🍚",
        "ケーキ": "🍰",
        "ピザ": "🍕",
        "ハンバーガー": "🍔",
        "ステーキ": "🥩",
        "カレー": "🍛",
        "寿司": "🍣",
        "パスタ": "🍝",
        "コーヒー": "☕",
        "ワイン": "🍷",
        "ビール": "🍺",
        "アイス": "🍦",
        "チョコレート": "🍫",
    }
    
    # ポジティブな感情キーワード（絵文字マップ）
    positive_emotions = {
        "楽しい": "楽しい😘",
       "楽しみ": "楽しみだネ🎵",
        "嬉しい": "嬉しい😍",
        "嬉しい": "嬉しい😍",
        "喜び": "喜び😍",
        "最高": "最高😍",
        "サイコー": "サイコー😍",
        "最強": "最強💪",
        "期待": "期待😍",
        "ドキドキ": "ドキドキ😘",
        "ワクワク": "ワクワク😍",
        "好き": "好き😘",
        "大好き": "大好き😍",
        "愛してる": "愛してる💕",
        "恋": "恋😍",
        "感謝": "感謝😍",
        "ありがとう": "ありがとう😘",
        "イケメン": "イケメン😎",
        "美人": "美人😍",
        "かわいい": "かわいい😘",
        "素敵": "素敵😍",
        "いいね": "いいね👍",
        "最高だ": "最高だ😍",
        "サイコー": "サイコー😍",
        "ナイス": "ナイス👍",
        "完璧": "完璧✨",
        "幸せ": "幸せ💕",
        "うれしい": "うれしい😍",
    }
    # 褒める（絵文字マップ）
    negative_emotions = {
        "すごい": "すごいネ‼️尊敬しちゃうナ✨",
        "可愛い": "可愛いネ❤️チュッ（笑）",
        "頑張れ": "頑張る君も素敵だヨ応援してるゾ❤️",
        
    }
   
    # ネガティブな感情キーワード（絵文字マップ）
    negative_emotions = {
        "悲しい": "悲しい😭",
        "辛い": "辛い😭",
        "困った": "困った😭",
        "寂しい": "寂しい😭",
        "怒り": "怒り💢",
        "怒": "おこだヨ💢",
        "怒ってる": "怒ってる💢",
        "怒ってる": "怒ってる💢",
        "つらい": "つらい😭",
        "苦しい": "苦しい😭",
        "嫌": "嫌😭",
        "最悪": "最悪😭",
        "つらいな": "つらいな😭",
        "泣く": "泣く😭",
        "うざい": "うざい🙄",
        "むかつく": "ムカつく😕", 
        "不安": "心配だヨ💦",
        "大丈夫": "大丈夫かナ❓",

    }
    
    # 会話的な反応キーワード
    reaction_keywords = {
        "わかった": "わかった👍",
        "了解": "了解👍",
        "了解です": "了解だヨ👍",
        "マジで": "マジで😲",
        "マジ": "マジ😲",
        "本当に": "本当に😲",
        "本当": "本当😲",
        "ホントに": "ホントに😲",
        "ホント": "ホント😲",
        "まじか": "まじか😲",
        "うそだろ": "うそだろ😲",
        "ウケる": "ウケる😂",
        "爆笑": "爆笑😂",
    }
    
    # 時間表現キーワード
    time_keywords = {
        "明日": "明日🌅",
        "明後日": "明後日🌅",
        "昨日": "昨日📅",
        "今夜": "今夜🌙",
        "毎日": "毎日📅",
        "朝から": "朝☀️から",
        "朝": "朝☀️",
        "夜中": "夜中🌙",
        "夜": "夜🌙",
    }
    
    # 文章全体の感情カウント（置き換え前）
    positive_count = sum(1 for word in positive_emotions.keys() if word in text)
    negative_count = sum(1 for word in negative_emotions.keys() if word in text)
    reaction_count = sum(1 for word in reaction_keywords.keys() if word in text)
    
    # ポジティブな感情キーワードに絵文字を付与（長い順）
    sorted_positive = sorted(positive_emotions.items(), key=lambda x: len(x[0]), reverse=True)
    for emotion, replacement in sorted_positive:
        text = text.replace(emotion, replacement)
    
    # ネガティブな感情キーワードに絵文字を付与（長い順）
    sorted_negative = sorted(negative_emotions.items(), key=lambda x: len(x[0]), reverse=True)
    for emotion, replacement in sorted_negative:
        text = text.replace(emotion, replacement)
    
    # 会話的な反応キーワードに絵文字を付与（長い順）
    sorted_reactions = sorted(reaction_keywords.items(), key=lambda x: len(x[0]), reverse=True)
    for reaction, replacement in sorted_reactions:
        text = text.replace(reaction, replacement)
    
    # 時間表現キーワードに絵文字を付与（長い順）
    sorted_times = sorted(time_keywords.items(), key=lambda x: len(x[0]), reverse=True)
    for time_word, replacement in sorted_times:
        text = text.replace(time_word, replacement)
    
    # 名詞に対応する絵文字（長い順でソート）
    noun_emoji_map = {
        "お返事": "💬",
        "チャン": "👧✨",
        "ちゃん": "👧✨",
        "くん": "👦✨",
        "氏": "🧑",
        "元気": "💪",
        "返事": "💬",
        "会社": "🏢",
        "仕事": "💼",
        "家": "🏠",
        "愛": ['❤️','💕',]
        "デート":  ['❤️','💕',]
        "恋":  ['❤️','💑','💖',]
        "キス": ['😘','💕','👄','💏',]
        "抱きしめる": "🤗",
        "手": "🤝",
        "腕": "💪",
        "目": "👀",
        "口": "👄",
        "頭": "🧠",
        "顔": "😊",
        "笑顔": "😊",
        "笑い": "😂",
        "笑う": "😂",
        "泪": "😭",
        "涙": "😭",
        "怒り": "💢",
        "拳": "✊",
        "指": "👆",
        "足": "🦵",
    }
    
    # 施設・場所の絵文字を追加（長い順）
    sorted_locations = sorted(location_emoji_map.items(), key=lambda x: len(x[0]), reverse=True)
    for location, emoji in sorted_locations:
        text = text.replace(location, location + emoji)
    
    # 食べ物・飲み物の絵文字を追加（長い順）
    sorted_foods = sorted(food_emoji_map.items(), key=lambda x: len(x[0]), reverse=True)
    for food, emoji in sorted_foods:
        text = text.replace(food, food + emoji)
    
    # 名詞の絵文字を追加（長い順）
    sorted_nouns = sorted(noun_emoji_map.items(), key=lambda x: len(x[0]), reverse=True)
    for noun, emoji in sorted_nouns:
        text = text.replace(noun, noun + emoji)
    
    # あいさつの判定
    greeting_morning = ["おはよう", "朝"]
    greeting_night = ["こんばんは", "おやすみ", "夜"]
    
    is_morning_greeting = any(greeting in text for greeting in greeting_morning)
    is_night_greeting = any(greeting in text for greeting in greeting_night)
    is_question = "？" in text
    
    # 文章の話題を判定（出現した絵文字・キーワードから）
    topic_analysis = {
        "グルメ・デート": [emoji for _, emoji in food_emoji_map.items()] + [emoji for _, emoji in location_emoji_map.items()],
        "愛情,好き，ラブ，愛してる，大好き": ["😘", "😍", "💕", "💛", "❤️", "♡"],
        "怒る,嫌い,きもい，悲しい，泣く，": ["😭", "💢", "🙄"],
    }
    
    topic_scores = {}
    for topic, emojis in topic_analysis.items():
        topic_scores[topic] = sum(text.count(emoji) for emoji in emojis)
    
    # 最も多い話題を取得
    dominant_topic = max(topic_scores.items(), key=lambda x: x[1])[0] if max(topic_scores.values()) > 0 else None
    
    # 疑問符の処理
    if is_question:
        text = text.replace("？", "？？")
    
    # 文章全体の感情に基づいて文末に絵文字を追加
    overall_emotion_emoji = ""
    if positive_count > negative_count:
        # ポジティブな感情が勝っている場合
        if positive_count >= 2:
            if dominant_topic == "グルメ・デート":
                overall_emotion_emoji = " 😍🍽️💕"
            else:
                overall_emotion_emoji = " 😍♡💛"
        else:
            overall_emotion_emoji = " 😘♡"
    elif negative_count > positive_count:
        # ネガティブな感情が勝っている場合
        if negative_count >= 2:
            overall_emotion_emoji = " 😭💢🙄"
        else:
            overall_emotion_emoji = " 😭🙄"
    
    # あいさつの場合は時間帯の絵文字を優先
    if is_morning_greeting:
        text += " ☀️"
    elif is_night_greeting:
        text += " 🌙"
    elif overall_emotion_emoji:
        text += overall_emotion_emoji
    
    return text


# --- ここからテスト用コード ---
if __name__ == "__main__":
    test_msg = "やっほー○○チャン！元気ですか？楽しみです。○○ちゃんはおじさんとデートするのが好きですよね？おじさんをたくさん喜ばしてほしいな。おじさんは毎日○○ちゃんのことばっかり考えてるよ。"
    
    print("--- おじさんモード ---")
    print(ojisan_converter(test_msg))
    print()
    
    # 敬語ではない通常の文章もテスト
    test_msg2 = "今日は楽しかった。君のことが好きだ。明日も会いたいね。"
    print("--- 通常のタメ口 ---")
    print("入力:", test_msg2)
    print("出力:", ojisan_converter(test_msg2))
    print()
    
    # 別のテスト例
    test_msg3 = "朝からずっと君のことばかり考えている。会いたい。"
    print("--- 別の例 ---")
    print("入力:", test_msg3)
    print("出力:", ojisan_converter(test_msg3))