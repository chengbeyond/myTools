def adjust_resolution(width_target, original_width, original_height):
    """
    调整分辨率以保持原有宽高比。

    :param width_target: 目标宽度
    :param original_width: 原始宽度
    :param original_height: 原始高度
    :return: 调整后的目标宽度和高度，保持原宽高比
    """
    # 计算宽度变化的比例
    width_ratio = width_target / original_width

    # 根据宽度比例计算新的高度
    height_target = int(original_height * width_ratio)

    return width_target, height_target


# 示例：将宽度调整为1920，保持1920x1080的宽高比
original_width = 1920
original_height = 1080
new_width = 2560  # 假设我们想把宽度调整为2560
adjusted_width, adjusted_height = adjust_resolution(new_width, original_width, original_height)

print(f"调整后的分辨率是：{adjusted_width}x{adjusted_height}")