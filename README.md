# 刘晔工作台

战术听力防护装备渠道开发工作台（PWA / 渐进式 Web 应用）。

本地直接打开 `刘晔工作台.html` 即可使用；站点已配置为可「添加到主屏幕」的 PWA，
可在 iPhone Safari、macOS Safari（添加到程序坞）、Windows Chrome/Edge（安装）中使用，
离线也能打开，数据保存在浏览器 localStorage，无需后端。

## 功能模块
- 今日任务
- 品牌新品监控（10 个核心品牌：3M PELTOR / HOWARD LEIGHT / WALKER'S / EARMOR / OTTO / INVISIO / AXIL / DECIBULLZ / OPS-CORE / SORDIN）
- 每日复盘
- 业务 SOP
- 年度销售计划（12 个月双色分组条形图：预期目标 vs 已达成）

## 部署（GitHub Pages）
1. 仓库根目录即站点，`index.html` 为入口（内容与 `刘晔工作台.html` 一致）。
2. 仓库 Settings → Pages → 选择 `main` 分支、`/`（root）发布。
3. 访问 `https://<用户名>.github.io/<仓库名>/`。

## 更新
修改 `刘晔工作台.html` 后，复制为 `index.html` 并重新推送即可生效。
图标由 `genicon.js`（Node）生成。
