# Master Prompt — Build with the Fluid Glass UI

请先读取本 Skill 包中的：

1. `SKILL.md`
2. `DESIGN_SYSTEM.md`
3. `references/canonical-reference.png`
4. `references/fluid-glass-material.css`
5. `references/canonical-vertex-shader.glsl`
6. `references/canonical-fragment-shader.glsl`
7. `references/fluid-glass-engine.js`
8. `ACCEPTANCE_CHECKLIST.md`

然后生成一个生产级的流体玻璃卡片页面。

## 强制要求

- 必须复用 Canonical Shader，不要重新设计 Shader；
- 必须复用 Canonical Material CSS 的几何和分层；
- 卡片高度固定为 `144px`，圆角为 `30px`；
- 移动端不得变成方形卡；
- 默认底材透明度为 `0.08`；
- WebGL Canvas 必须透明，禁止整卡不透明大理石纹；
- 默认 Cyan 颜色必须严格使用：
  - `#00E7D2`
  - `#3CC8FF`
  - `#075F68`
- 不允许出现大面积暖黄色、橄榄色和米黄色；
- 流体必须左侧克制、中右侧活跃；
- 必须保留鼠标扰动、质量档位、CSS fallback、保存与导出；
- 卡片 ID / key 必须来自配置，不得绑定固定业务字段；
- 图表扩展默认关闭。用户没有明确要求时，不生成折线图。

## 可修改内容

你可以修改：

- 卡片数量；
- 卡片 key；
- 标题、数值、单位；
- 品牌名称；
- 页面外壳；
- A/B/C；
- surface、speed、intensity、pointer、seed；
- 存储键。

## 不可修改内容

你不得修改：

- Shader 核心公式；
- reveal 空间遮罩；
- plume1 / plume2；
- Canvas Alpha 机制；
- 材质层级；
- 默认卡片几何；
- 默认 Cyan 色相范围。

## 完成后

1. 运行页面；
2. 与 `references/canonical-reference.png` 对照；
3. 按 `ACCEPTANCE_CHECKLIST.md` 逐项检查；
4. 输出最终源码和验收结果。
