# 内存段可视化工具开发日志

## 需求分析

原始需求：
```
0. 请建个文件，保持记录我们沟通的内容，方便追溯

1.我要做一个小工具，用图表直观的显示内存段的地址和段名

2.输入是一个jason文件，内容有两类格式
2.1 起始地址和长度
2.2 起始地址和终止地址

3.输出是一个漂亮，直观的图表

4.如果我jason文件中的地址，不是按照大小排列的，请输出图表时，自动帮我排列

5.如果有段地址重叠时，也请直观的显示
```

## 开发过程

### 第一版实现

首先创建了基本项目结构：
- memmap_visualizer.py
- requirements.txt
- README.md
- example.json

实现了基本的功能：
- 解析JSON文件中的内存段信息
- 支持两种输入格式：起始地址+长度 和 起始地址+终止地址
- 自动排序内存段
- 使用水平条形图显示内存段
- 标记重叠区域

### 第二版改进

修复了十六进制格式化错误：
```
ValueError: Unknown format code 'x' for object of type 'float'
```

通过添加正确的格式化函数解决了这个问题：
```python
def format_hex(x, p):
    """将数值格式化为十六进制字符串"""
    return f'0x{int(x):x}'
```

### 第三版优化

根据反馈，修改了可视化方式：
- 使用一维数轴来展示内存段
- 每个段用不同颜色的线段表示
- 显示段名和地址

### 第四版修复

添加了中文字体支持：
```python
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
```

### 第五版改进

针对重叠段的处理：
- 将重叠的段放在不同行显示
- 使用垂直虚线连接相关段

修复了数字类型解析错误：
```python
def hex_to_int(hex_str):
    """将十六进制字符串转换为整数，同时支持数字类型"""
    if isinstance(hex_str, int):
        return hex_str
    elif isinstance(hex_str, str):
        return int(hex_str, 16)
    else:
        raise TypeError(f"不支持的类型: {type(hex_str)}")
```

### 最终版本

根据最后的反馈进行了优化：
- 移除了顶部黑线
- 减小了行间距
- 使用柔和的亮色调色板
- 优化了连接线显示
- 更新了README.md文件

## 功能总结

最终实现的功能：
1. 支持两种格式的内存段描述：起始地址+长度和起始地址+终止地址
2. 支持字符串和数字类型的地址和长度值
3. 自动排序和处理重叠的内存段
4. 使用柔和的亮色显示不同的内存段
5. 清晰显示每个段的名称和地址
6. 自动生成美观的可视化图表

## 使用示例

测试文件（example.json）：
```json
{
    "segments": [
        {
            "name": "代码段",
            "start": "0x1000",
            "length": "0x1000"
        },
        {
            "name": "数据段",
            "start": "0x2000",
            "end": "0x3000"
        },
        {
            "name": "堆栈段",
            "start": "0x1500",
            "length": "0x800"
        }
    ]
}
```

运行命令：
```bash
python memmap_visualizer.py example.json
```

输出：生成了一个名为`example_visualization.png`的图片文件，展示了内存段的分布情况。 