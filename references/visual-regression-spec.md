# Visual Regression Specification

对照文件：`canonical-reference.png`

## 检查维度

1. 卡片高度与圆角；
2. 暗背景透出程度；
3. 左侧内容保护区；
4. 中右侧流体集中度；
5. Cyan 色相是否偏冷；
6. 是否出现黄色或橄榄色；
7. 是否出现高频大理石纹；
8. 颗粒是否轻微；
9. 边缘高光是否克制。

## 建议截图环境

- viewport: `1400 × 600`
- device scale factor: `1`
- 等待动画约 2–3 秒后截图
- 默认 surface: `0.08`
- quality: `balanced` 或 `high`

## 失败条件

- 流体覆盖整张卡；
- 卡片接近正方形；
- 主体出现暖黄色；
- 视觉更像大理石 / 油画而不是透明光学流体。
