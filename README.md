# Friendship-Faker
LINEのトーク履歴を用いてAIがトーク相手の性格や口調を忠実に再現し、偽の相手と会話をすることができます。

## 使い方
IOS版のLINEからトーク履歴のtxtファイルを抽出し、保存します。
そのtxtファイルのファイルパスを**file_path**に入力します・
**assistant_name**にはAIに演じさせたい方のLINEの名前を入力します。
**user_name**には自分がなりたい方のLINEの名前を入力します。
```py
if __name__ == "__main__":
    file_path = "test.txt" # トーク履歴のファイルパス
    assistant_name = "assistant" # 相手の名前
    user_name = "user" # 自分の名前
    main(file_path, assistant_name, user_name)  # メイン処理を実行
```
実行すると入力を求められます。メッセージを送信するとトークが開始します.

## 使用用途
- **バラエティとして遊ぶ**(本来の目的)
- 会話のシミュレーション
  - 会話の練習
  - 本人に言いたいことを言ってみる
    - ストレス発散
    - どう会話が展開するか確認
- 相手との関係性をAIの解釈で確認する
- 自分をAIに演じさせて自分自身と会話してみる
  - 相手から見た自分を確認できる

## 注意
- ローカルLLMではなくインターネットを介したサービスを使用していますので第三者がトーク内容を閲覧できる可能性があります
- 倫理的に考えてバラエティ以外の目的で使用することはお勧めしません。会話は相手がどのように返すか分からないから面白いのです
- IOS版やPC版などではトークデータのフォーマットが違います。現段階ではIOS版LINEのフォーマットのみサポートしてます。Android版は確認できる環境ではないため分かりません
