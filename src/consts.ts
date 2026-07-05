// 公式LINE 友だち追加URL（全CTA・ヘッダー・フッターで共有）
// 変更時はこの1箇所だけ直せば全ボタンに反映される
export const LINE_URL = "https://lin.ee/N7kXEsR";

// Microsoft Clarity プロジェクトID（clarity.microsoft.com で取得する10文字前後の英数字）
// 空文字のあいだは計測タグを一切読み込まない＝安全な無効状態
// 本番ビルド（astro build / Vercel）のときだけ計測する（ローカル開発のアクセスは集計しない）
export const CLARITY_PROJECT_ID = "x9tovaddyn";
