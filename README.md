# 内存段可视化工具

这是一个用于可视化内存段地址和段名的工具，它能够直观地展示不同内存段的分布情况。

## 功能特点

- 支持两种输入格式：
  1. 起始地址和长度（十六进制字符串或数字）
  2. 起始地址和终止地址（十六进制字符串或数字）
- 自动对内存段按地址大小进行排序
- 自动检测并在不同行显示重叠的内存段
- 使用柔和的亮色调显示不同内存段
- 清晰显示每个段的起始和结束地址（十六进制格式）
- 生成美观、直观的可视化图表

## 使用方法

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 准备输入JSON文件，格式如下：
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
            "length": 2048
        }
    ]
}
```

3. 运行程序：
```bash
python memmap_visualizer.py input.json
```

4. 查看生成的图表：
程序会生成一个名为 `input_visualization.png` 的图片文件，其中展示了内存段的分布情况。

## 中文字体问题解决方案

如果您在运行程序时看到如下错误：
```
findfont: Generic family 'sans-serif' not found because none of the following families were found: SimHei
```

这表示您的系统中没有安装程序所需的中文字体。解决方法如下：

### Windows用户
Windows通常已经安装了SimHei(黑体)字体，无需额外操作。

### macOS用户
macOS用户可以通过以下步骤解决：
1. 安装系统自带的中文字体：在"系统设置" > "语言与区域" > "键盘偏好设置"中，添加中文输入法
2. 使用Homebrew安装开源中文字体：
   ```bash
   # 安装Homebrew (如果尚未安装)
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # 安装Source Han Sans字体
   brew tap homebrew/cask-fonts
   brew install --cask font-sourcehan-sans
   ```
3. 或手动安装字体：
   - 下载[思源黑体](https://github.com/adobe-fonts/source-han-sans/releases/latest)
   - 双击下载的字体文件安装到系统
   
4. 安装字体后重新启动程序

### Linux用户
Linux用户可以安装相应的中文字体包：
- Ubuntu/Debian：
  ```bash
  sudo apt-get install fonts-wqy-microhei
  ```
- CentOS/Fedora：
  ```bash
  sudo yum install wqy-microhei-fonts
  ```

安装字体后，可能需要清除matplotlib的字体缓存：
```bash
rm -rf ~/.matplotlib/*.cache
```

## 注意事项

- 地址可以使用十六进制字符串（如"0x1000"）或直接使用数字（如4096）
- 重叠的内存段会自动放置在不同的行上
- 每个段都会用不同的柔和色彩显示，便于区分
- 图表会清晰显示每个段的起始和结束地址

## 示例输出

执行命令：
```bash
python memmap_visualizer.py example.json
```

会生成一个直观的内存段可视化图表，显示各个内存段的分布和关系。 