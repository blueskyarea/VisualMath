# 走行する電車内で見える雨

東向きに `4.0 m/s` で走る電車内の人が、地面に対して鉛直下向きに降る雨を見る。
電車内では、雨が鉛直方向から `30 deg` 傾いて見える問題を可視化する。

## 相対速度

雨を地面から見た速度、電車を地面から見た速度、雨を電車内の人から見た速度の間には、

\[
\vec{v}_{\text{rain/train}}
=\vec{v}_{\text{rain/ground}}-\vec{v}_{\text{train/ground}}
\]

という関係がある。

東を `x` 軸の正、上を `y` 軸の正とする。雨の地面に対する落下速度を `v` とすると、

\[
\vec{v}_{\text{rain/ground}}=(0,-v),\qquad
\vec{v}_{\text{train/ground}}=(4,0)
\]

なので、電車内で見える雨の速度は

\[
\vec{v}_{\text{rain/train}}=(-4,-v)
\]

となる。鉛直方向との角が `30 deg` より、

\[
\tan30^\circ=\frac{4}{v}
\]

したがって、

\[
\boxed{v=4\sqrt3\ \mathrm{m/s}\simeq6.92\ \mathrm{m/s}}
\]

## 実行

プロジェクト直下で実行する。

```bash
python3 rain-on-train/rain_on_train.py
```

左図では地面から見た雨と電車の速度を、右図では電車内の人から見た雨の速度を表示する。
緑の斜めの矢印の水平成分が `4.0 m/s`、鉛直成分が雨の実際の落下速度である。
