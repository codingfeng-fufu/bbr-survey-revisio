# M02：BBR系统综述检索与筛选协议 v1（冻结）

冻结日期：2026-09-28。执行人：Codex；最终范围与正文采纳由冯宗林审核。

## 检索来源

本轮首先使用两个无需机构登录、可保存完整请求参数的公开索引：

1. OpenAlex works API：保存请求URL、日期、结果总数和原始JSON。
2. Crossref works API：保存请求URL、日期、结果总数和原始JSON。

这两个来源用于重建本轮可复现检索。后续如作者能够访问Scopus、Web of Science、IEEE Xplore或ACM DL，再按本协议增加来源，不覆盖本轮日志。

## 查询组

| query_id | 主题 | 查询字符串 |
|---|---|---|
| Q1 | BBR总体 | `BBR congestion control` |
| Q2 | BBRv2/v3 | `BBRv2 BBRv3 congestion control` |
| Q3 | RTT公平性 | `BBR RTT fairness` |
| Q4 | 缓冲区与丢包 | `BBR buffer loss ECN` |
| Q5 | BDP-Veno | `BDP-Veno` |
| Q6 | OVeno | `OVeno TCP congestion control` |
| Q7 | 无线/卫星 | `BBR wireless satellite LEO` |
| Q8 | AI拥塞控制 | `learning congestion control fairness` |

查询字符串按原样发送。不同来源的字段语法和命中数分开记录，不把两个来源的总数直接相加。

## 时间范围

检索执行日为2026-09-28；记录索引返回的发表日期，保留最早可用记录至检索日。协议、源码和技术资料另存版本或访问日期。检索结果不预设最终纳入数，不要求保持原稿的165篇。

## 纳入标准

记录至少涉及一个研究问题，并属于：BBR机制/版本资料；BBR性能、公平性、时延、重传、缓冲区、丢包、ECN或网络场景研究；相关综述或比较研究；BDP-Veno/OVeno等相关BDP型TCP；AI/学习辅助拥塞控制研究；支撑网络、队列、BDP或复现实验定义的规范资料。

## 排除标准

题名/摘要与研究问题无关；重复报告；无法取得正文且无法判断用途；纯宣传材料；没有可核查来源；与本文AI、公平性或服务差异问题无关。排除时记录一个主要理由。正文中已经引用不能作为纳入标准。

## 记录和筛选单位

- `record_id`：一次索引导出的记录。
- `report_id`：具体论文、报告、规范或源码资料。
- `study_id`：同一研究的多个报告集合。

先保存原始记录，再按 DOI、标准化标题、作者和年份去重。题名/摘要筛选后再全文筛选。未取得全文单独标记，不写成全文排除。

## 冻结后的变更规则

任何新查询、来源、时间范围或纳入标准都建立v2并写明理由。v1结果保留，不覆盖原始文件。OpenAlex/Crossref是本轮公开索引证据，不等同于已完成Scopus、Web of Science、IEEE或ACM的机构数据库检索。
