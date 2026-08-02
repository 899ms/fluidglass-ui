# Acceptance Checklist

## Canonical Core

- [ ] 实现直接复用了 `canonical-fragment-shader.glsl`。
- [ ] 实现直接复用了 `fluid-glass-material.css` 的核心几何和分层。
- [ ] 未自行重新发明 Shader。
- [ ] 未删除 `reveal`、`plume1`、`plume2`。

## Geometry

- [ ] 卡片高度为 `144px`。
- [ ] 卡片圆角为 `30px`。
- [ ] 桌面横向宽卡。
- [ ] 移动端仍为横向 144px 高，不是正方形。

## Material

- [ ] 默认 surface 为 `0.08`。
- [ ] WebGL Canvas 使用透明背景。
- [ ] context 使用 `alpha:true`。
- [ ] context 使用 `premultipliedAlpha:false`。
- [ ] 使用 `gl.clearColor(0,0,0,0)`。
- [ ] 左侧明显比右侧更透明。
- [ ] 暗色页面背景可透过卡片。

## Color

- [ ] 默认 A/B/C 分别为 `#00E7D2 / #3CC8FF / #075F68`。
- [ ] 默认效果没有大面积黄色、米色、橄榄色和橙色。
- [ ] 没有随机色相旋转。

## Fluid Shape

- [ ] 流体是低频、柔和、有机的形变。
- [ ] 不是高频大理石纹。
- [ ] 不是整张油画纹理。
- [ ] 不是几个 blur 圆。
- [ ] 流体主要位于中右侧。
- [ ] 鼠标可产生局部卷动和推开。

## Chart Boundary

- [ ] 默认 `chart.enabled = false`。
- [ ] 未经明确要求没有添加折线图。
- [ ] 若启用图表，颜色只来自 A/B/C 冷色体系。

## Generic Configuration

- [ ] 卡片 key 来自配置。
- [ ] 没有固定业务 ID。
- [ ] 没有内部项目名称、内部版本号或内部存储键。
- [ ] 卡片数量可配置。

## Engineering

- [ ] localStorage 正常。
- [ ] HTML 导出正常。
- [ ] Auto / High / Balanced / Eco / Fallback 正常。
- [ ] WebGL 失败自动 CSS fallback。
- [ ] prefers-reduced-motion 正常。
- [ ] 页面隐藏时不绘制。
- [ ] 控制台无错误。

## Visual Regression

- [ ] 已与 `references/canonical-reference.png` 对照。
- [ ] 卡片比例、透明度、流体分布和色相接近参考图。
