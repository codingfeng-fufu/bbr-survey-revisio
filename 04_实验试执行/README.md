# 实验试执行文件说明

先读[试执行报告](试执行报告.md)。本目录记录设计展开与本机环境检查，尚未进行TCP流量实验。

| 文件 | 用法 |
|---|---|
| design_matrix_liuxinyue_DRAFT.csv | 刘馨月32个配置、160次候选运行；不是实际运行顺序 |
| design_matrix_all_DRAFT.csv | 全组52个配置、260次候选运行，供统筹核对 |
| E3_predictions_TO_FILL.csv | 冯宗林填写8个网络条件的预测、容差和冻结版本 |
| example_config_DRAFT.json | 配置示例，UNRESOLVED字段仍须落实 |
| run_metrics_EMPTY.csv | 空结果模板，运行后才填写实测结果 |
| design_validation.json | 程序检查结果，real_experiments_executed为0 |
| build_design.py | 生成设计文件并检查算术/配对的脚本，不是网络实验运行脚本 |

不要在填好预测或结果后直接重跑生成脚本：它会重写同名设计与模板文件。需要重新生成时先复制脚本到新的版本目录运行，保留已填写的记录。

CSV可用表格软件打开，采用UTF-8 BOM。正式开跑前须确认Linux机器、固定协议实现、队列实现、采集流程、质量门槛和冻结配置；E3另需先保存预测。
