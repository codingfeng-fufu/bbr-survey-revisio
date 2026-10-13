# 图表、排版与AI披露问题台账

| 问题 | 证据 | 处理 | 状态 |
|---|---|---|---|
| 完整zip主稿存在7个overfull | `zip_full_compile_20261012.log` | 在Overleaf逐页定位并修表格/图注 | 待处理 |
| 完整zip主稿存在62个underfull | 同上 | 结合PDF视觉检查，非全部必须修复 | 待处理 |
| 2个hyperref empty-anchor警告 | 同上 | 检查摘要/作者/锚点位置 | 待处理 |
| Figure 2–6图号与caption映射 | `figure_inventory_20261012.csv` | 对照Overleaf主版本确认 | 待验收 |
| AI工具和用途 | `figure_provenance_20261012.csv` | 原制图者提供事实 | 待确认 |
| 实验图与四实现数据一致 | `cross_version_20261012/` | 冯宗林签收 | 待验收 |

后续完整编译必须针对当前候选整合版本；历史zip警告不能代替新稿检查。AI模型/用途已在候选声明标明待作者确认，尚未签收。WLAN错误倍数表已撤回，图源对应数据仍待确认。


2026-10-13 Mathis范围修正：候选正文改为Reno-like近似，注明ACK/稳态/超时及接收窗口限制；撤回CUBIC通用15Mbps上限、由公式推出1/10MB阈值、BDP保证优势及固定133倍结论。原始WAN数值需原始测量条件再次核验后才能恢复。


2026-10-13模型范围修正：滤波窗口明确限定BBRv1及packet-timed rounds；撤回未逐版本核验的v2/v3统一5s参数。cwnd改为简化目标近似；删除保证真实路径估计、避免浅队列溢出及ProbeRTT保证无队列等绝对表述。Startup判据改为带宽增长而非gain下降，ECN能力与实际启用分开。
