# BBR版本、参数与ECN机制验收（F05/F11）

| 实现 | 身份证据 | 运行时名 | 本批次ECN | 说明 |
|---|---|---|---|---|
| Ubuntu baseline | Ubuntu in-tree kernel record | `bbr` | off | 不命名为BBRv1 |
| BBRv1 module | `tcp_bbr1.c` + compatibility patch | `bbr1` | off | 本项目6.13模块构建 |
| BBR2 | `5.13.12-bbr2alpha` manifest | `bbr2` | off | 独立内核 |
| BBRv3 | `BBR_VERSION=3`, `6.13.7-bbr3` | `bbr` | off | 独立内核 |

## 必须保留的措辞

- ECN关闭只说明测试配置，不等于 BBRv2/v3 退化为 BBRv1。
- 未观测的内部变量不能由吞吐差异伪造轨迹。
- BBRv1 module 的本地 TSO 兼容补丁必须在方法和限制中标注。

## 证据路径

`formal_bbr1_20261012/manifest.json`、`formal_bbr2_20261010/manifest.json`、`formal_bbr3_20261011/manifest.json`、`formal_random_loss_20261012/`。
