# 文旅联合资料湖的分支三方合并与冲突发布

文旅联合资料以不可变快照组织。graph.py 管理有向提交图，catalog.py 保存命名分支与带代号的比较交换，reader.py 提供按提交读取。现有发布入口只接收单一父版本。

运行环境为 Python 3.11。代码只使用标准库，数据位于 data/sample.json。
包内的 __main__.py 运行现有组件并输出其实际处理结果。

```sh
python3 -m branchlake
python3 -m unittest discover -s tests -v
python3 -m compileall -q branchlake tests
```

文件职责与数据约定见 contracts.md。测试使用临时目录，不改写项目内的数据。
