# -*- coding: utf-8 -*-


def trancking_plot1(info, servo_manager):
    x, y, w, h = info
    center_x = int(w / 2)
    center_y = int(h / 2)
    dif_x = x - center_x
    dif_y = y - center_y
    """
    * 当dif_x>0时，代表底部舵机该往右转;
    * 当dif_x<0时，代表底部舵机该往左转;
    * 当dif_y>0时，代表上部舵机该往下转;
    * 当dif_y<0时，代表上部舵机该往上转.
    """

    """
    策略一: 根据dif的大小，限定step
    1280/10=128
    720/10=72
    """
    # todo 可以根据人脸大小的策略....  切割画面 分更多段搞
    x_thread = 40
    y_thread = x_thread
    nums = [1, 8, 12]
    # nums = [1, 10, 20]

    if abs(dif_x) < x_thread:
        x_step = 0
    elif x_thread <= abs(dif_x) <= w / 2 * 1 / 3:
        x_step = nums[0]
    elif w / 2 * 1 / 3 < abs(dif_x) <= w / 2 * 2 / 3:
        x_step = nums[1]
    else:
        x_step = nums[2]

    if abs(dif_y) < y_thread:
        y_step = 0
    elif abs(dif_y) <= h / 2 * 1 / 3:
        y_step = 1
        # y_step = int(nums[0] * 0.5625)
    elif h / 2 * 1 / 3 < abs(dif_y) <= h / 2 * 2 / 3:
        y_step = int(nums[1] * 0.5625)
    else:
        y_step = int(nums[2] * 0.5625)

    if dif_x > 0 and dif_y > 0:
        # 底部舵机右转(+)&上部舵机下转(+)
        # print("底部舵机右转(+)&上部舵机下转(+)")
        servo_manager.moveA(x_step, y_step)
    elif dif_x < 0 and dif_y > 0:
        # 底部舵机左转(-)&上部舵机下转(+)
        # print("底部舵机左转(-)&上部舵机下转(+)")
        servo_manager.moveA(-x_step, y_step)
    elif dif_x > 0 and dif_y < 0:
        # 底部舵机右转(+)&上部舵机上转(-)
        # print("底部舵机右转(+)&上部舵机上转(-)")
        servo_manager.moveA(x_step, -y_step)
    elif dif_x < 0 and dif_y < 0:
        # 底部舵机左转(-)&上部舵机上转(-)
        # print("底部舵机左转(-)&上部舵机上转(-)")
        servo_manager.moveA(-x_step, -y_step)
