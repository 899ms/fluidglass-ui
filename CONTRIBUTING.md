# 贡献指南

感谢你对 **Fluid Glass UI** 的关注。本项目是一个面向编码 Agent 的流体玻璃界面生成技能包，采用 Apache-2.0 许可证开源。

在提交 PR 之前，请先阅读本文档，特别是「核心约束」一节——本项目的贡献规则与普通前端库有明显差异。

---

## 一、核心约束：Canonical Material Core

本项目的设计哲学是 **「固定视觉内核 + 开放业务配置」**。其中「固定视觉内核」由下面这组文件构成，我们称之为 **Canonical Material Core**：

| 文件 | 作用 |
| --- | --- |
| `references/canonical-fragment-shader.glsl` | 流体材质片元着色器（FBM、Domain Warp、Reveal、Plumes） |
| `references/canonical-vertex-shader.glsl` | 顶点着色器 |
| `references/fluid-glass-material.css` | 玻璃分层、卡片几何、透明度预算 |
| `references/fluid-glass-engine.js` | WebGL 运行时引擎、鼠标扰动、降级逻辑 |
| `references/canonical-reference.png` | 视觉基准参考图 |
| `references/canonical-demo-single-file.html` | 单文件参考实现 |

**为什么要特别谨慎？**

所有下游项目（以及所有安装了本技能包的 Agent）都以这些文件作为视觉真理来源。任何一处像素级改动都会同时改变全部下游产物的观感，导致跨项目视觉一致性被破坏，且这种破坏往往在很久之后才被发现。

因此，涉及 Canonical Material Core 的 PR 会走**更严格的 review 流程**：需要附带前后对比截图，并说明改动对 `canonical-reference.png` 基准的影响。这类 PR 的合并速度会明显慢于普通 PR，请理解。

`CANONICAL_CORE_HASHES.json` 记录了这 6 个文件的 sha256 与字节数，CI 会强制校验。

---

## 二、欢迎的改动

以下类型的贡献我们非常欢迎，可以直接提 PR：

- **文档改进**：修正错别字、补充说明、改善示例、翻译。
- **Bug 修复**：修复引擎逻辑错误、内存泄漏、事件监听未解绑等问题。
- **浏览器兼容性增强**：Safari / 移动端 WebGL 差异、`webgl2` 回退到 `webgl`、无 WebGL 环境下的降级表现。
- **新配色预设**：以**新增**预设的形式提供，不改动默认色板。
- **性能优化**：在不改变渲染结果的前提下降低 GPU / CPU 开销，例如减少 uniform 上传次数、优化 resize 节流、`IntersectionObserver` 暂停离屏渲染。

---

## 三、需要充分讨论的改动

以下改动会影响视觉内核的语义，**请先开 Issue 讨论并达成共识后再动手**，避免白做：

- 修改 Shader 核心公式（FBM 层数与权重、Domain Warp 强度、Reveal 曲线、Plumes 分布）。
- 改变卡片几何：卡片高度 `144px`、圆角 `30px`。
- 改变默认色板。
- 改变材质分层结构（玻璃层顺序、透明度预算、模糊半径的分配方式）。

即使你确信改动是「更好看的」，也请先讨论——本项目优先保证一致性，其次才是主观美感。

---

## 四、提交 PR 前的检查清单

请逐项确认，并在 PR 描述中勾选：

1. **运行自检脚本**

   ```bash
   python tools/package_qa.py
   ```

   输出中必须包含 `"passed": true`，且退出码为 `0`。

2. **同步哈希清单（仅当修改了 canonical 核心文件时）**

   若你改动了第一节表格中的任意文件，必须同步更新 `CANONICAL_CORE_HASHES.json`，否则 CI 会失败。可以用以下命令自动重新生成：

   ```bash
   python tools/package_qa.py --update-hashes
   ```

   更新后请再跑一次普通模式确认通过，并在 PR 中说明为什么需要改动核心文件。

3. **浏览器实机验证**

   用浏览器实际打开 `references/canonical-demo-single-file.html`，确认：
   - 流体材质渲染正常，动画流畅；
   - 鼠标移动时扰动响应正确；
   - 控制台无任何报错或警告。

4. **对照验收清单自检**

   逐条对照 `ACCEPTANCE_CHECKLIST.md` 检查，确保没有破坏既有约定。

5. **更新变更记录**

   在 `CHANGELOG.md` 中追加本次改动条目。

---

## 五、代码风格

- **JavaScript**：2 空格缩进，字符串使用单引号，语句结尾加分号，避免引入任何构建依赖（本项目坚持零依赖、可直接在浏览器打开）。
- **Python**：遵循 PEP 8，4 空格缩进，行宽建议不超过 100 字符。
- **文档**：中文与英文、数字之间加一个空格，例如「卡片高度 144px 不可修改」。
- **GLSL / CSS**：保持与现有文件一致的缩进与命名风格，不做无关的格式化改动（格式化 diff 会让 review 极其困难）。

---

## 六、提交 Issue 的建议

报告 Bug 时，请尽量提供以下信息，这能极大加快定位速度：

- **浏览器与版本**：例如 Chrome 131.0.6778.86 / Safari 18.1；
- **操作系统**：例如 Windows 11 / macOS 15.1 / iOS 18；
- **显卡型号与驱动**：例如 NVIDIA RTX 3060 / Apple M2 / Intel Iris Xe（WebGL 问题高度依赖 GPU）；
- **控制台完整报错**：包括堆栈信息，不要只贴一行；
- **复现步骤**：从打开哪个文件开始，到出现问题的最小操作路径；
- **截图或录屏**：视觉类问题请务必附上，并说明「期望是什么样」。

提交功能建议时，请说明使用场景与它为什么不能通过现有的配置项实现。

---

## 七、许可证

提交贡献即表示你同意你的贡献以 [Apache-2.0](./LICENSE) 许可证发布。
