# Component API

## 配置模型

卡片以数组配置，`key` 由调用方提供或自动生成：

```js
{
  key: "revenue-summary",
  label: "Revenue",
  eyebrow: "MONTHLY",
  value: "12.8M",
  unit: "USD",
  change: 8.4,
  preset: "cyan",
  a: "#00e7d2",
  b: "#3cc8ff",
  c: "#075f68",
  speed: 0.92,
  intensity: 1.02,
  pointer: 0.82,
  surface: 0.08,
  seed: 1.7,
  chart: { enabled: false }
}
```

`key` 不是产品固定 ID，使用者可以使用自己的业务键。

## 运行时 API

```js
window.FluidGlassMaterial.getConfig()
window.FluidGlassMaterial.getStatus()
window.FluidGlassMaterial.openSettings(key?)
window.FluidGlassMaterial.closeSettings()
window.FluidGlassMaterial.save()
window.FluidGlassMaterial.exportHtml()
window.FluidGlassMaterial.pause()
window.FluidGlassMaterial.resume()
window.FluidGlassMaterial.setQuality(value)
window.FluidGlassMaterial.setPalette(key, preset)
window.FluidGlassMaterial.setColors(key, a, b, c)
window.FluidGlassMaterial.setSurface(key, value)
window.FluidGlassMaterial.setMotion(key, patch)
```

## 预设

- `cyan`
- `original`
- `klein`
- `chrome`

## 应用到全部卡片

只能同步：

- `a`
- `b`
- `c`
- `surface`
- `preset`

不得同步每卡独立运动参数。
