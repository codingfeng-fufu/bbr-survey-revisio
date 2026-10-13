# 开放全文实际获取记录

本轮检查12个公开PDF入口，取得9个可解析PDF；3个403失败。保留原URL、最终跳转、字节数、SHA256、PDF解析状态与提取文本。ResearchSquare的latest链接可能指向不同修订版，实际最终URL须核对，不直接沿用索引版本。

下载/解析成功不等于题名、作者、DOI身份匹配或全文资格审查通过。队列状态为pdf_acquired_identity_pending，最终纳入不改变。正文定量结果还需页/图/表核查。当前日志第1批无逐请求时间戳，只确认在2026-10-12本轮取得；后续脚本已添加UTC请求时间。

## 首页面身份核对

已检查9份提取文本的首页题名、作者区和标识信息，其中8份首页包含记录对应DOI（见identity_review.csv）；LEO handover论文记录无DOI，仍待机构仓储的发表/版本记录确认。这不是全文资格验收。

DA-BBR记录的DOI含2019，但首页同时记载2019-12在线发表与2020-01当前版本，年份引用须区分。IEICE QUIC/ECN文件首页明确为advance publication，并提示终版将替换；即使DOI一致，也不能把版面上的临时卷号当作最终书目信息。ResearchSquare两份当前PDF封面DOI均与v1记录一致，仍需检查后续正式版/撤稿状态和研究重复关系。

## 完整队列覆盖

执行 `python 06_执行台账/build_complete_acquisition_queue.py` 从完整资格队列和原始索引导出重建公开入口，再运行fetch_open_fulltexts.py。当前1860待审报告组中732组有索引归档入口；入口可能是DOI网页，不等于开放PDF或访问成功。其余记录需另行元数据/作者仓储定位，不能因缺链接排除。旧400行队列及已完成资格证据保持不变。

成功取得的报告现在按规范化DOI（缺DOI时按题名）跨批次跳过，不因canonical record ID变更重新获取。相同记录ID若返回不同PDF内容，将用内容哈希后缀另存，保留既有文件；不同来源版本仍需人工身份/版本审查。此次完成语法检查，未新增网络下载或资格判断。

## Bounded acquisition and incremental evidence

Per-file reads now enforce a45-second overall network deadline checked between read1 chunks, with10-second socket waits; pdfinfo/pdftotext have15/30-second subprocess limits. The overall deadline may be exceeded by one bounded socket operation. Each finished request atomically updates the retrieval log, so a slow remaining request does not hide completed source evidence. These limits are acquisition controls, not reasons to exclude a paper. Syntax checked; no new batch launched during this change.
