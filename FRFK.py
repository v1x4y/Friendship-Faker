import json  # JSON操作のためのライブラリをインポート
import re  # 正規表現操作のためのライブラリをインポート
import requests  # HTTPリクエストを送信するためのライブラリをインポート
import datetime  # 日付と時刻を操作するためのライブラリをインポート
import pytz  # タイムゾーンを操作するためのライブラリをインポート

# ローカル時間を取得する関数
def get_localtime():
    now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))  # 現在の日時を取得し、日本時間に変換
    week_days_jp = ["月", "火", "水", "木", "金", "土", "日"]  # 日本語の曜日リストを作成
    formatted_date = now.strftime("%Y/%m/%d") + "(" + week_days_jp[now.weekday()] + ")"  # 日付と曜日をフォーマット
    return str(formatted_date)  # フォーマットされた日付を文字列として返す

# チャットログをJSON形式に変換する関数
def convert_chat_to_json(file_path, assistant_name, user_name):
    with open(file_path, 'r', encoding='utf-8') as f:
        chat_log = f.read()  # チャットログを読み込む

    lines = chat_log.splitlines()  # チャットログを行ごとに分割

    output = []  # 出力用のリストを初期化
    last_role = None  # 前回の役割を初期化
    for line in lines:
        # 空行や特定のメッセージをスキップ
        if not line.strip() or line.endswith("がメッセージの送信を取り消しました"):
            continue

        if ":" in line:
            time, rest_of_line = line.split("	", 1)  # 時刻と残りの行を分割
            if "	" in rest_of_line:
                user, message = rest_of_line.split("	", 1)  # ユーザーとメッセージを分割
                if (message.startswith("[") and message.endswith("]")) or message.startswith("☎"):
                    continue  # 特定の形式のメッセージをスキップ
                role = None  # 役割を初期化
                if user == user_name:
                    role = "user"  # ユーザーの場合は"user"
                elif user == assistant_name:
                    role = "assistant"  # アシスタントの場合は"assistant"
                else:
                    continue  # それ以外の場合はスキップ

                # メッセージをまとめる
                if role == last_role and output:
                    output[-1]["content"] += "\n" + message.strip()  # 前回の役割と同じ場合はメッセージを追加
                else:
                    output.append({"role": role, "content": message.strip()})  # 新しいメッセージを追加

                last_role = role  # 最後の役割を更新
        elif re.match(r'\d{4}\/\d{2}\/\d{2}.+', line):
            output.append({"role": "system", "content": line})  # システムメッセージを追加

    return output  # 処理結果を返す

# チャットメッセージをAPIに送信し、返信を取得する関数
def api_chat(message, log):
    api = f"https://x-4.jp/api/v1/chat/claude/haiku?message={message}"  # APIエンドポイントを設定
    res = requests.post(api, json=log)  # APIにPOSTリクエストを送信
    response = res.json()  # レスポンスをJSON形式で取得
    return response["choices"][0]["message"]  # レスポンスからメッセージを取得して返す

# メイン処理
def main(file_path, assistant_name, user_name):
    chat_data = convert_chat_to_json(file_path, assistant_name, user_name)  # チャットログをJSON形式に変換
    chat_data.append({"role": "system", "content": f"{get_localtime()}\n上記はLineのトーク内容です。これからの会話でも引き続き違和感のないように振舞ってください。\nassistantの名前: {assistant_name}\nuserの名前: {user_name}"})  # システムメッセージを追加
    while True:
        text = input(f"{user_name}: ")  # ユーザーからの入力を受け取る
        if text:
            try:
                response = api_chat(text, chat_data)  # チャットメッセージをAPIに送信し、返信を取得
                chat_data.append(response)  # レスポンスをチャットデータに追加
                print(f"{assistant_name}: {response['content']}")  # アシスタントの返信を表示
            except Exception as e:
                print(f"エラーが発生しました: {e}")  # エラーが発生した場合はエラーメッセージを表示
                break
        else:
            break

if __name__ == "__main__":
    file_path = "test.txt" # トーク履歴のファイルパス
    assistant_name = "assistant" # 相手の名前
    user_name = "user" # 自分の名前
    main(file_path, assistant_name, user_name)  # メイン処理を実行
