# Fluid Glass UI

[![License](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)

[English](README.md) · **中文**

**WebGL 流体玻璃卡片界面生成器**：固定视觉内核（Canonical Material Core）+ 开放、数据驱动的业务配置。既是一个可安装到编码 Agent 的**技能包**，也是一份**零依赖的前端参考实现**。

用现代浏览器直接打开[单文件 Demo](references/canonical-demo-single-file.html)，即可看到效果：透明流体玻璃卡片、鼠标扰动、优雅的 CSS 降级。

![流体玻璃动效演示](docs/demo.gif)

## 这是什么

大多数「glassmorphism 提示词」每次生成结果都会漂移。本项目把设计反了过来：**视觉材质固定为 Canonical 内核**，业务相关内容全部可配置。

- **固定（Canonical Material Core）**：卡片几何（144px 高、30px 圆角）、玻璃分层顺序、透明度预算、WebGL Shader（FBM + Domain Warp + Reveal + Plumes）、鼠标扰动、CSS 降级路径。
- **开放（业务配置）**：卡片数量、标题、数值、单位、配色、预设、动效、质量档位、`localStorage` 存储键。

任何下游项目——或任何加载了本技能包的 Agent——都会得到相同的视觉基因，由哈希校验的核心资产和自动化 QA 门禁保障。

## 特性

- **WebGL1 流体 Shader** — FBM + Domain Warp，`alpha:true` 透明画布，`gl.clearColor(0,0,0,0)`
- **指针扰动** — 鼠标/触控推动流体流动
- **质量档位** — `auto / high / balanced / eco / fallback`
- **CSS 降级** — WebGL 不可用或达到上下文预算时自动切换
- **WebGL 上下文预算** — 最多 8 个活跃上下文（适配 iOS Safari）；超出的卡片走 CSS 降级
- **零依赖** — 无 CDN、无外部字体、无网络请求；`file://` 直接可跑
- **数据驱动卡片** — 最多 12 张卡、任意 `key`、可选图表扩展（默认关闭）
- **运行时控制** — `window.FluidGlassMaterial.*` API 控制配色、质量、动效、导出
- **`localStorage` 持久化** 与 **一键导出 HTML**
- **性能卫生** — 统一 RAF 管理器、页面隐藏暂停、`ResizeObserver`、`IntersectionObserver`、`prefers-reduced-motion`

## 快速开始

### 1. 直接看效果

```bash
# 直接打开单文件 Demo（无需服务器、无需构建）
start references/canonical-demo-single-file.html    # Windows
open references/canonical-demo-single-file.html     # macOS / Linux
# 或模块化版本
open references/canonical-demo.html
```

### 2. 作为 Agent 技能使用

1. 把整个目录复制到 Agent 的技能目录（入口为 `SKILL.md`，见 `manifest.json`）。
2. 让 Agent「做一个流体玻璃指标卡看板」。
3. Agent 必须按 `SKILL.md` 执行：读取 `references/` 下的 Canonical 资产、复用它们、按 `ACCEPTANCE_CHECKLIST.md` 自检。

若 Agent 不支持自动加载技能，可把 `MASTER_PROMPT.md`（完整版）或 `QUICK_START_PROMPT.md`（精简版）全文作为提示词。

### 3. 集成到现有前端

拷贝三个核心资产，构造卡片数组：

```bash
references/fluid-glass-material.css     # 材质 + 几何
references/canonical-fragment-shader.glsl
references/canonical-vertex-shader.glsl
references/fluid-glass-engine.js        # FluidGlassRenderer / FluidGlassManager / materialTokens() / qualityProfile()
```

完整的集成注意事项（需要深色背景、144px 高度固定、Alpha 预算约束）与变更流程见 [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)。

## 配置

卡片是一个普通数组。`key` 由调用方提供（或自动生成）——绝不是固定业务 ID。

```json
{
  "storageKey": "fluid_glass_material_config",
  "quality": "auto",
  "interaction": true,
  "cards": [
    {
      "key": "revenue-summary",
      "label": "Revenue",
      "eyebrow": "MONTHLY",
      "value": "12.8M",
      "unit": "USD",
      "change": 8.4,
      "preset": "cyan",
      "a": "#00e7d2",
      "b": "#3cc8ff",
      "c": "#075f68",
      "speed": 0.92,
      "intensity": 1.02,
      "pointer": 0.82,
      "surface": 0.08,
      "seed": 1.7,
      "chart": { "enabled": false }
    }
  ]
}
```

- JSON Schema：[CONFIG_SCHEMA.json](CONFIG_SCHEMA.json)
- 品牌中立示例：[REFERENCE_CONFIG.json](REFERENCE_CONFIG.json)
- 字段语义 + 运行时 API：[COMPONENT_API.md](COMPONENT_API.md)
- 预设：`cyan`、`original`、`klein`、`chrome`

### 运行时 API

引擎加载完成后暴露：

```js
FluidGlassMaterial.getConfig() / getStatus()
FluidGlassMaterial.openSettings() / closeSettings()
FluidGlassMaterial.save() / exportHtml() / pause() / resume()
FluidGlassMaterial.setQuality(v)
FluidGlassMaterial.setPalette(key, preset)
FluidGlassMaterial.setColors(key, a, b, c)
FluidGlassMaterial.setSurface(key, v)
FluidGlassMaterial.setMotion(key, { speed?, intensity?, pointer? })
```

## 项目结构

```
fluidglass-ui/
├── SKILL.md                  # Agent 技能入口（YAML frontmatter 不可删）
├── MASTER_PROMPT.md          # 完整任务提示词
├── QUICK_START_PROMPT.md     # 精简提示词
├── DESIGN_SYSTEM.md          # 不可变视觉内核 vs 可配置边界
├── COMPONENT_API.md          # 配置模型 + 运行时 API
├── CONFIG_SCHEMA.json        # JSON Schema
├── REFERENCE_CONFIG.json     # 品牌中立示例配置
├── ACCEPTANCE_CHECKLIST.md   # 一致性验收清单
├── INTEGRATION_GUIDE.md      # 集成与变更流程
├── CANONICAL_CORE_HASHES.json# 内核文件 sha256 清单
├── README.md                 # 英文 README
├── README.zh-CN.md           # 中文 README
├── CHANGELOG.md
├── manifest.json
├── docs/
│   ├── demo.gif              # 动效演示（README 头图）
│   └── brand/                # 作者品牌资产（保留版权，不随 Apache-2.0）
│       ├── xiaoce-avatar.jpg
│       └── README.md         # 品牌许可声明
├── references/               # Canonical Material Core + 参考实现
│   ├── canonical-fragment-shader.glsl
│   ├── canonical-vertex-shader.glsl
│   ├── fluid-glass-material.css
│   ├── fluid-glass-engine.js
│   ├── canonical-demo.html            # 模块化 Demo
│   ├── canonical-demo-single-file.html# 单文件 Demo（直接打开）
│   ├── canonical-reference.png        # 视觉基准图
│   └── visual-regression-spec.md      # 截图回归规范
└── tools/
    └── package_qa.py         # 包完整性与内核自检（无第三方依赖）
```

## 质量门禁

```bash
python tools/package_qa.py          # 必须输出 "passed": true
python tools/package_qa.py --update-hashes   # 改内核后重新生成哈希清单
node --check references/fluid-glass-engine.js
```

CI（[.github/workflows/qa.yml](.github/workflows/qa.yml)）会在每次 push/PR 上运行同样的门禁。修改任何 Canonical 内核文件**必须**重新生成 `CANONICAL_CORE_HASHES.json`，并对照 `references/canonical-reference.png` 提交前后对比截图——详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 浏览器支持

- 支持 WebGL1 的桌面与移动浏览器（Chrome、Edge、Firefox、Safari）——流体 Shader。
- 不支持 WebGL 的浏览器——自动 CSS 降级。
- **上下文预算**：引擎最多同时持有 8 个 WebGL 上下文（iOS Safari 安全上限）。9–12 卡布局中，第 9 张起走 CSS 降级。
- 单次配置卡片上限为 12。

## 参与贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。欢迎 Bug 修复、文档改进、浏览器兼容性工作与新增**追加式**配色预设。涉及视觉内核的改动走更严格的 review：先开 Issue 讨论、提交对比截图、同步哈希、QA 全绿。

## 许可证

[Apache-2.0](LICENSE) © 2026 csuyincs-creator（清晨方白晓）。提交贡献即表示你同意你的贡献以相同许可证发布。[`docs/brand/`](docs/brand/) 下的品牌资产为保留版权，**不随 Apache-2.0 授权**。

## 作者

![作者头像](docs/brand/xiaoce-avatar.jpg)

**清晨方白晓** · [csuyincs-creator](https://github.com/csuyincs-creator) · 中南工科研究生 · 非 AI 从业者，热衷探索 AI 落地实践与 Vibe Coding，持续记录分享好玩的东西。

- 公众号🔍：**清晨方白晓**
- 小红书 / 抖音同号：**清晨方白晓**

小策角色形象为作者个人 IP——详见 [品牌声明](docs/brand/README.md)。
