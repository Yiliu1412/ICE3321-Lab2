import os
import matplotlib.pyplot as plt
import numpy as np
import load_trace
import fixed_env as env
import bba

def plot_results(trace_files):
    # 加载网络带宽 trace
    all_cooked_time, all_cooked_bw, all_file_names = load_trace.load_trace()

    # 初始化环境
    net_env = env.Environment(all_cooked_time=all_cooked_time, all_cooked_bw=all_cooked_bw)

    for trace_idx, trace_file in enumerate(trace_files):
        if trace_idx >= len(all_cooked_time):
            print(f"Trace file {trace_file} not found in the loaded traces.")
            continue

        # 初始化变量
        time_stamp = 0
        buffer_sizes = []
        bit_rates = []
        bandwidths = []
        time_stamps = []

        last_bit_rate = bba.DEFAULT_QUALITY
        bit_rate = bba.DEFAULT_QUALITY

        while True:
            # 获取视频块信息
            delay, sleep_time, buffer_size, rebuf, video_chunk_size, next_video_chunk_sizes, end_of_video, video_chunk_remain = net_env.get_video_chunk(bit_rate)

            # 更新时间戳
            time_stamp += delay
            time_stamp += sleep_time

            # 记录数据
            buffer_sizes.append(buffer_size)
            bit_rates.append(bba.VIDEO_BIT_RATE[bit_rate])
            bandwidths.append(net_env.cooked_bw[net_env.mahimahi_ptr - 1])
            time_stamps.append(time_stamp / 1000.0)  # 转换为秒

            # 更新码率选择逻辑
            if buffer_size < bba.RESERVOIR:
                bit_rate = 0
            elif buffer_size >= bba.RESERVOIR + bba.CUSHION:
                bit_rate = bba.A_DIM - 1
            else:
                bit_rate = (bba.A_DIM - 1) * (buffer_size - bba.RESERVOIR) / float(bba.CUSHION)
            bit_rate = int(bit_rate)

            if end_of_video:
                break

        # 绘制图像
        plt.figure(figsize=(15, 12))

        # 网络带宽
        plt.subplot(3, 1, 1)
        plt.plot(time_stamps, bandwidths, label="Bandwidth (Mbps)", color="blue", linewidth=2)
        plt.xlabel("Time (s)", fontsize=12)
        plt.ylabel("Bandwidth (Mbps)", fontsize=12)
        plt.title(f"Trace: {trace_file} - Bandwidth", fontsize=14, fontweight='bold')
        plt.xlim(0, max(time_stamps))  # 固定 x 轴从 0 开始
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(loc="upper right", fontsize=10)

        # 缓冲区大小
        plt.subplot(3, 1, 2)
        plt.plot(time_stamps, buffer_sizes, label="Buffer Size (s)", color="orange", linewidth=2)
        plt.xlabel("Time (s)", fontsize=12)
        plt.ylabel("Buffer Size (s)", fontsize=12)
        plt.title(f"Trace: {trace_file} - Buffer Size", fontsize=14, fontweight='bold')
        plt.xlim(0, max(time_stamps))  # 固定 x 轴从 0 开始
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(loc="upper right", fontsize=10)

        # 码率选择
        plt.subplot(3, 1, 3)
        plt.plot(time_stamps, bit_rates, label="Bitrate (Kbps)", color="green", linewidth=2)
        plt.xlabel("Time (s)", fontsize=12)
        plt.ylabel("Bitrate (Kbps)", fontsize=12)
        plt.title(f"Trace: {trace_file} - Bitrate Selection", fontsize=14, fontweight='bold')
        plt.xlim(0, max(time_stamps))  # 固定 x 轴从 0 开始
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(loc="upper right", fontsize=10)

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    # 选取三个网络带宽 trace 文件
    trace_files = ["norway_bus_1", "norway_car_1", "norway_ferry_1"]
    plot_results(trace_files)