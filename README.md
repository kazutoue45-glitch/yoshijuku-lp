# 義塾LP（yoshijuku-lp）

寝屋川市成田町の学習塾「義塾（よしじゅく）」の集客LP。

## 公開URL

https://kazutoue45-glitch.github.io/yoshijuku-lp/

## 構成

- Astro 5（ゼロ依存・シングルページ）
- スマホファースト・1カラム
- 9セクション構成 + 5箇所インラインCTA

## 開発

```bash
npm install
npm run dev          # ローカル開発サーバ
npm run build        # ./docs に静的ファイル出力（GitHub Pages公開先）
```

## ワイヤーモック

`wireframes/` 配下にCodex CLI image_genで生成したセクションごとのモックアップ画像。
実装の視覚指針として使用。

## デプロイ

`main/docs` を GitHub Pages の公開元に設定。
`npm run build` の出力が `docs/` に入るため、コミット&pushで自動公開される。
