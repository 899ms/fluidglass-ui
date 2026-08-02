# Design System — Canonical Fluid Glass Material

## 核心原则

通用性不等于视觉自由。视觉一致性由固定材质内核保证，通用性由配置和 API 保证。

## 不可变 Token

| Token | 标准值 |
|---|---:|
| Card height | `144px` |
| Card radius | `30px` |
| Default surface | `0.08` |
| Glass blur | `16px` |
| Canvas scale | `1.035` |
| Canvas blur | `1.8px` |
| Noise opacity | `0.075` |
| Default A | `#00E7D2` |
| Default B | `#3CC8FF` |
| Default C | `#075F68` |

## 固定空间构图

- 左侧：内容保护区，流体可见度低；
- 中部：平滑过渡；
- 右侧：主要流体 plume 与色团；
- 边缘：轻微 fade，不能硬切；
- 流体不应填满整个 Canvas。

## Alpha 预算

- Canvas 背景透明；
- 非流体区接近 Alpha 0；
- 主要流体 Alpha 上限约 0.92；
- reveal 决定左右分布；
- surfaceOpacity 只参与高白底适配，不能把 Canvas 变成不透明底图。

## 禁止视觉

- 高频大理石纹；
- 油画颜料纹；
- 云海铺满整卡；
- 黄色荧光液体；
- 方形卡片；
- 粗重边框；
- 默认折线图；
- 全屏随机色相旋转。

## 响应式

- 桌面：4 列；
- 中屏：2 列；
- 小屏：1 列；
- 所有断点都保持 `144px` 卡片高度；
- 不允许为了单列而把卡片拉成正方形。

## 图表扩展

图表是可选扩展，不属于 Canonical Material Core。默认关闭。
