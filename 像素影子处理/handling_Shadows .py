import os
from PIL import Image


def change_shadow_color(image_path, output_path, old_color, new_color):
    # 打开图像
    img = Image.open(image_path)

    # 将图像转换为RGBA模式，以便处理透明度
    img = img.convert("RGBA")

    # 加载图像数据
    datas = img.getdata()

    # 创建一个新的数据列表
    new_data = []

    # 遍历每个像素
    for item in datas:
        # 检查像素是否为特定绿色
        if item[:3] == old_color[:3]:  # 比较RGB值
            # 替换为淡黑色，确保透明度被正确处理
            new_data.append((new_color[0], new_color[1], new_color[2], item[3]))
        else:
            new_data.append(item)

    # 更新图像数据
    img.putdata(new_data)

    # 保存更改后的图像
    img.save(output_path)


def process_images_in_folder(folder_path, output_folder, old_color, new_color):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 检查文件是否为图片（这里假设图片扩展名为 .png）
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            input_path = os.path.join(folder_path, filename)
            output_path = os.path.join(output_folder, f'processed_{filename}')
            change_shadow_color(input_path, output_path, old_color, new_color)


# 定义颜色值
old_color = (15, 127, 37)  # 绿色 #0F7F25
new_color = (60, 60, 60)  # 淡黑色，不包括透明度

# 使用示例
process_images_in_folder('.', 'done', old_color, new_color)
