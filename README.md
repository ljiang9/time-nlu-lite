# time-nlu-lite

零依赖的中文时间自然语言解析。把「下周三下午三点」「明天早上」「晚上」之类口语换算成结构化日期时间，基于给定当前时间做相对推算。

## 快速开始

```bash
python -m time_nlu_lite "下周三下午三点"
python -m time_nlu_lite "明天早上"
python -m time_nlu_lite "晚上" --base "2026-10-06 10:00"
```

## 无 API Key 如何运行

纯规则解析，离线运行，不需要任何 API Key。

## 运行测试

```bash
python -m unittest discover -s tests -v
```

## License

MIT © ljiang9
