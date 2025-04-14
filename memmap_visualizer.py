import json
import sys
import platform
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Tuple
import matplotlib.patches as patches
import matplotlib.colors as mcolors

# 设置中文字体
system = platform.system()
if system == 'Windows':
    plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows系统
elif system == 'Darwin':  # macOS
    # 更新macOS字体列表，按照更可能存在的顺序排列
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Heiti TC', 'STHeiti', 'PingFang SC']
else:  # Linux等系统
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'Droid Sans Fallback', 'AR PL UMing CN']
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号

# 额外的字体配置，使用matplotlib的内置回退方案
try:
    # 尝试导入matplotlib的字体管理模块
    from matplotlib import font_manager
    # 清理字体缓存的现代方法，而不是使用_rebuild
    import os
    import shutil
    cache_dir = font_manager.get_cachedir()
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir, ignore_errors=True)
        print(f"已清理字体缓存目录: {cache_dir}")
    # 让matplotlib重新加载字体
    font_manager._load_fontmanager()
except Exception as e:
    print(f"字体配置警告: {e}")
    print("将尝试使用默认字体渲染")

def hex_to_int(hex_str):
    """将十六进制字符串转换为整数，同时支持数字类型"""
    if isinstance(hex_str, int):
        return hex_str
    elif isinstance(hex_str, str):
        return int(hex_str, 16)
    else:
        raise TypeError(f"不支持的类型: {type(hex_str)}")

def parse_segment(segment: Dict) -> Tuple[str, int, int]:
    """解析内存段数据，返回段名、起始地址和结束地址"""
    name = segment['name']
    start = hex_to_int(segment['start'])
    
    if 'length' in segment:
        length = hex_to_int(segment['length'])
        end = start + length
    else:
        end = hex_to_int(segment['end'])
    
    return name, start, end

def format_hex(x, p):
    """将数值格式化为十六进制字符串"""
    return f'0x{int(x):x}'

def detect_overlaps(segments: List[Tuple[str, int, int]]) -> Dict[int, int]:
    """检测段重叠并确定每个段应该在哪一行显示"""
    segments_sorted = sorted(segments, key=lambda x: x[1])  # 按起始地址排序
    rows = {}  # 每个段应该在哪一行
    row_end = {}  # 每一行的结束位置
    
    for i, (name, start, end) in enumerate(segments_sorted):
        # 找到一个没有重叠的行
        row = 0
        while row in row_end and start < row_end[row]:
            row += 1
        
        rows[i] = row
        row_end[row] = end
    
    return rows

def visualize_memory_map(json_file: str):
    """可视化内存段"""
    # 读取JSON文件
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 解析所有内存段
    segments = [parse_segment(seg) for seg in data['segments']]
    
    # 按起始地址排序
    segments.sort(key=lambda x: x[1])
    
    # 确定每个段的显示行
    segment_rows = detect_overlaps(segments)
    max_row = max(segment_rows.values()) if segment_rows else 0
    
    # 创建图表，根据行数调整高度
    fig_height = 1.5 + max_row * 0.6  # 减小行间距
    fig, ax = plt.subplots(figsize=(15, fig_height))
    
    # 获取地址范围
    min_addr = min(seg[1] for seg in segments)
    max_addr = max(seg[2] for seg in segments)
    
    # 设置x轴范围，留出一些边距
    margin = (max_addr - min_addr) * 0.05
    ax.set_xlim(min_addr - margin, max_addr + margin)
    
    # 使用柔和的亮色调色板
    # 创建一个柔和的亮色调色板
    pastel_colors = [
        '#FF9AA2',  # 浅粉红
        '#FFB7B2',  # 浅橙红
        '#FFDAC1',  # 浅杏色
        '#E2F0CB',  # 浅黄绿
        '#B5EAD7',  # 浅薄荷
        '#C7CEEA',  # 浅蓝紫
        '#F2D4D7',  # 浅玫瑰
        '#A2E1DB',  # 浅绿松
        '#D4F0F7',  # 浅天蓝
        '#CCEAED',  # 浅蓝绿
    ]
    
    # 检查当前字体配置是否支持中文 - 此处简化检测方法
    can_display_chinese = True
    try:
        from matplotlib.font_manager import findfont, FontProperties
        # 更可靠的方法检测中文字体是否可用
        fonts = plt.rcParams['font.sans-serif']
        font_found = False
        
        # 尝试找到一个可用的字体
        for font in fonts:
            try:
                fp = FontProperties(family=font)
                if findfont(fp) != findfont(FontProperties()):
                    font_found = True
                    print(f"使用字体: {font}")
                    break
            except:
                continue
                
        if not font_found:
            print("警告: 无法找到合适的中文字体，正在使用系统默认字体")
            can_display_chinese = False
    except Exception as e:
        print(f"字体检测警告: {e}")
        can_display_chinese = False
    
    # 绘制内存段
    for i, (name, start, end) in enumerate(segments):
        row = segment_rows[i]
        row_y = -row * 0.6  # 每行的y坐标，减小行间距
        
        # 计算段的宽度和中心位置
        width = end - start
        
        # 绘制段区域
        rect = patches.Rectangle((start, row_y-0.1), width, 0.2, 
                                linewidth=1, edgecolor='black', 
                                facecolor=pastel_colors[i % len(pastel_colors)])
        ax.add_patch(rect)
        
        # 在段的中间添加段名
        middle = start + width/2
        ax.text(middle, row_y, name, ha='center', va='center', fontsize=9)
        
        # 添加起始和结束地址标签
        ax.text(start, row_y-0.18, f'0x{start:x}', rotation=45, 
               ha='right', va='top', fontsize=7)
        ax.text(end, row_y-0.18, f'0x{end:x}', rotation=45,
               ha='left', va='top', fontsize=7)
        
        # 如果不是第一行（row=0），绘制连接线
        if row > 0:
            # 绘制连接到上一行的虚线
            ax.plot([start, start], [row_y+0.1, -(row-1)*0.6-0.1], 'k--', alpha=0.3)
            ax.plot([end, end], [row_y+0.1, -(row-1)*0.6-0.1], 'k--', alpha=0.3)
    
    # 在x轴上标记关键地址点
    key_points = sorted(set([seg[1] for seg in segments] + [seg[2] for seg in segments]))
    for point in key_points:
        ax.text(point, 0.05, f'0x{point:x}', ha='center', va='bottom', rotation=45, fontsize=7)
    
    # 设置y轴范围和隐藏y轴
    ax.set_ylim(-max_row*0.6-0.3, 0.2)
    ax.set_yticks([])
    
    # 添加标题
    plt.title('内存段分布图')
    
    # 去除边框
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    
    # 隐藏x轴刻度
    ax.set_xticks([])
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    output_file = json_file.rsplit('.', 1)[0] + '_visualization.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"可视化结果已保存为: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法: python memmap_visualizer.py <input.json>")
        sys.exit(1)
    
    visualize_memory_map(sys.argv[1]) 