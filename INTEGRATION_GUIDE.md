# Integration Guide

## 1. 安装到编码 Agent

把整个目录作为一个技能包放进 Agent 的 skills 目录，例如：

- Claude Code / CodeBuddy Code：`~/.claude/skills/fluidglass-ui/` 或项目内 `.claude/skills/`
- 其他支持技能包的 Agent：放到其技能扫描目录，入口由 `manifest.json` 的 `entry` 指定，即 `SKILL.md`

`SKILL.md` 顶部的 YAML frontmatter 决定 Agent 能否自动识别与按需加载，请勿删除 `name` 与 `description`。`name` 必须与 `manifest.json` 的 `name` 保持一致。

安装后触发方式：直接描述需求即可，例如「做一个流体玻璃指标卡看板」。Agent 应按 `SKILL.md` 第 7 节的顺序执行：读需求 → 读 Skill → 看 `references/canonical-reference.png` → 复用 Canonical 资产 → 按 `ACCEPTANCE_CHECKLIST.md` 自检。

若 Agent 不支持自动加载，可手工把 `MASTER_PROMPT.md` 全文作为提示词，或用 `QUICK_START_PROMPT.md` 的单段版本。

## 2. 集成到现有前端项目

### 方式 A：复用三件套（推荐）

适合已有构建体系的项目：

1. 拷贝 `references/fluid-glass-material.css` 到样式目录，整体引入，不要按需裁剪其中的 CSS 变量与层级定义。
2. 拷贝 `references/canonical-vertex-shader.glsl` 与 `references/canonical-fragment-shader.glsl`，通过打包器的 raw/text 导入，或内联为字符串常量。
3. 拷贝 `references/fluid-glass-engine.js`，使用其中导出的 `FluidGlassRenderer`、`FluidGlassManager`、`materialTokens()`、`qualityProfile()`。
4. 按 `COMPONENT_API.md` 的配置模型构造卡片数组，字段结构参考 `REFERENCE_CONFIG.json`，约束以 `CONFIG_SCHEMA.json` 为准。
5. 运行时通过 `window.FluidGlassMaterial.*` 控制配色、质量档位与设置面板。

注意事项：

- 卡片容器必须允许 `144px` 固定高度，不要被父级 flex/grid 拉伸或压缩。
- 页面背景需为深色，否则玻璃分层与 `0.08` 底材透明度会失真。
- 不要给 Canvas 或卡片再叠加不透明背景，会破坏 Alpha 预算。
- 无 CDN、无外部字体、无网络请求是本包的既定约束，集成时保持一致。

### 方式 B：改造单文件 Demo

适合快速验证、静态页或不想引入构建链的场景：

1. 复制 `references/canonical-demo-single-file.html`，直接用浏览器打开确认基线效果。
2. 只替换业务外壳：品牌文案、卡片标题/数值/单位/变化值、卡片数量、`localStorage` 存储键。
3. `references/canonical-demo.html` 是模块化版本，需要拆分文件时以它为起点。

## 3. 可自定义范围

可以改：

- 品牌名称与页面文案；
- 卡片数量（1–12）与卡片 `key`；
- 标题、数值、单位、变化值等业务内容；
- 配色预设与 A/B/C 三色；
- `surface / speed / intensity / pointer / seed`；
- 全局质量档位与鼠标交互开关；
- `localStorage` 存储键；
- 是否启用可选图表扩展（默认关闭）。

不建议改：

- **Canonical Fragment Shader**：改动后不再保证与 `canonical-reference.png` 的视觉一致性，也会导致 `tools/package_qa.py` 的内核检查失败；
- `reveal` 左右空间控制、`plume1 / plume2`、`u_surfaceOpacity` 等 uniform；
- Canvas 的 `alpha:true`、`premultipliedAlpha:false`、`gl.clearColor(0,0,0,0)`；
- 卡片几何 `144px` 高、`30px` 圆角与材质七层结构；
- 默认 Cyan 的冷色相范围。

需要更强的视觉差异时，优先调 A/B/C 与 `surface / intensity`，而不是改 Shader。

## 4. 如何贡献变更

一般改动（文档、示例配置、业务外壳）：提 Issue 说明场景，或直接提 PR。

涉及 Canonical Core（Shader / Material CSS / Engine）的改动，必须完成以下步骤，否则 PR 无法合入：

1. 同步更新 `CANONICAL_CORE_HASHES.json` 中对应文件的哈希；
2. 按 `references/visual-regression-spec.md` 的截图环境（viewport `1400 × 600`、scale factor `1`、等待 2–3 秒、surface `0.08`、quality `balanced` 或 `high`）重新生成并替换 `references/canonical-reference.png`；
3. 运行 `python tools/package_qa.py`，确认输出 `"passed": true`；
4. 在 PR 描述中附改动前后的对照截图，并说明为何必须改内核；
5. 在 `CHANGELOG.md` 记录本次变更。

## 5. 命名与信息卫生

对外发布的产物中不要暴露内部项目名称、内部版本号或内部存储键。命名建议保持品牌中立，例如：

- Fluid Glass UI
- Fluid Glass UI Skill
- WebGL Fluid Glass Interface Kit

`ACCEPTANCE_CHECKLIST.md` 的 Generic Configuration 一节包含对应的自检项，`tools/package_qa.py` 也会扫描已知的内部标识串。
