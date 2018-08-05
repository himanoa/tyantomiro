# tyantomiro

## これなに？

ちゃんとみろはYoutubeAPIを用いてVTuberの配信をキャッチしDiscordで通知するBotの予定地です

## 動かし方

1. `.env` に以下の項目を記述。

```
DISCORD_TOKEN={DISCORDのアプリケーショントークン}
YOUTUBE_TOKEN={YOUTUBE_APIのトークン}
NOTIFY_CHANNEL_ID={通知したいDiscordのChannelId}
SUBSCRIBED_CHANNNEL_IDS={購読したいYoutubeのチャンネルID(,で区切ると複数個登録できる)}
```

2. `docker build -t tyantomiro .` を実行
3. `docker run -itd tyantomiro` を実行

## LICENSE

MIT
