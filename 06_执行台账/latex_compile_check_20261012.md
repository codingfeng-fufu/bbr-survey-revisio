# LaTeX 编译检查（2026-10-12）

## 工具

- `pdflatex`: TeX Live 2022/dev, pdfTeX 3.141592653-2.6-1.40.22
- `latexmk`: 4.76
- 安装记录：`/home/ubuntu/bbr3-build/apt_texlive_20261012.log`

## 完整候选稿

仓库候选副本命令：`latexmk -pdf -interaction=nonstopmode -halt-on-error cas-sc-template_F05_applied.tex`

结果：直接编译先因缺少 `cas-sc.cls` 停止。随后仅在 `/tmp` 使用官方 CAS 模板 class 做诊断，编译推进到正文后在首个缺失图 `optimal_operating_point.png` 停止。候选目录同时没有主稿引用的图片和 `refs.bib`，因此当前仓库副本不能代表 Overleaf 的完整编译环境。未把外部 class、占位图片或参考文献写入项目。

日志：`06_执行台账/full_candidate_compile_20261012.log`、`06_执行台账/full_candidate_compile_with_cas_20261012.log`。

临时 CAS class 诊断还报告了 185 个未解析 citation、14 个未解析 cross-reference，以及若干 overfull/underfull 警告；这些数字不能在缺少 `refs.bib` 和原图的情况下作为最终排版结论。

## 用户提供的完整项目

压缩包：`/home/ubuntu/BBRComputerNetworks (1).zip`，SHA256：`710c728377b312eb3098e8962c5a68099059b147c89d8ce3fa4615677521caa9`。

临时解压目录中的 `cas-sc-template.tex` 使用了配套 `cas-sc.cls`、`refs.bib` 和全部图片，命令 `latexmk -pdf -interaction=nonstopmode cas-sc-template.tex` 成功，生成 28 页 PDF。最终日志没有未解析 citation 或 reference；发现 7 个 overfull、62 个 underfull，以及 2 个 hyperref empty-anchor 警告。

- 完整编译日志：`06_执行台账/zip_full_compile_20261012.log`
- 临时 PDF：`/tmp/bbr_revision_compile_20261012/zip_project/cas-sc-template.pdf`
- 临时 PDF SHA256：`09784cd31fd6487499751a5353e4f6686f0f593b6e2361057dde1cf9cc37a5b1`

该 zip 主稿与仓库中的 `cas-sc-template_F05_applied.tex` 不是字节相同版本；编译结果证明用户提供的完整项目可编译，不能自动证明候选修改已合入该主稿。

## E3 候选片段

使用标准 `article` 编译器具包装入 `F13_E3_results_candidate.tex` 和 `F15_cross_version_results_candidate.tex`，执行两轮 `latexmk` 后成功生成 1 页 PDF。修正了案例编号和文件名下划线未转义问题；最终编译没有新的 `Overfull` 或 `Underfull` 警告。

临时 PDF：`/tmp/bbr_revision_compile_20261012/e3/compile_check_e3_20261012.pdf`。

这只证明候选片段的 LaTeX 语法和表格结构可编译，不代表完整 CAS 稿件已经通过排版验收。
