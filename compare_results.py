import os
import matplotlib.pyplot as plt
import numpy as np

def parse_log_file(log_file_path):
    """解析日志文件，提取时间戳、码率、缓冲区大小和奖励"""
    time_stamps = []
    bit_rates = []
    buffer_sizes = []
    rewards = []

    with open(log_file_path, 'r') as f:
        for line in f:
            if line.strip():  # 跳过空行
                data = line.split('\t')
                time_stamps.append(float(data[0]))  # 时间戳
                bit_rates.append(float(data[1]))  # 码率
                buffer_sizes.append(float(data[2]))  # 缓冲区大小
                rewards.append(float(data[6]))  # 奖励

    return time_stamps, bit_rates, buffer_sizes, rewards


def compare_results(result_dirs, target_trace):
    """比较多个结果文件夹中的日志文件"""
    plt.figure(figsize=(15, 10))

    for result_dir in result_dirs:
        # 适配不同算法生成的日志文件
        log_files = [os.path.join(result_dir, f) for f in os.listdir(result_dir) 
                     if (f.startswith('log_sim_bb') or f.startswith('log_sim_rb')) and f.endswith(f"_{target_trace}")]

        print(f"Checking directory: {result_dir}")
        print(f"Matched log files: {log_files}")

        if not log_files:
            print(f"No log files found in {result_dir} for trace {target_trace}")
            continue

        aggregated_rewards = []

        for log_file in log_files:
            print(f"Parsing log file: {log_file}")
            time_stamps, bit_rates, buffer_sizes, rewards = parse_log_file(log_file)

            if not time_stamps or not bit_rates or not buffer_sizes:
                print(f"No data to plot for {log_file}")
                continue

            aggregated_rewards.append(np.mean(rewards))  # 计算平均奖励

            # 绘制码率随时间变化图
            plt.subplot(3, 1, 1)
            plt.plot(time_stamps, bit_rates, label=f"{os.path.basename(result_dir)} - {os.path.basename(log_file)}")
            plt.xlabel("Time (s)")
            plt.ylabel("Bitrate (Kbps)")
            plt.title("Bitrate over Time")
            plt.grid(True)
            plt.legend()  

            # 绘制缓冲区大小随时间变化图
            plt.subplot(3, 1, 2)
            plt.plot(time_stamps, buffer_sizes, label=f"{os.path.basename(result_dir)} - {os.path.basename(log_file)}")
            plt.xlabel("Time (s)")
            plt.ylabel("Buffer Size (s)")
            plt.title("Buffer Size over Time")
            plt.grid(True)
            plt.legend() 

        if aggregated_rewards:
            # 绘制平均奖励柱状图
            plt.subplot(3, 1, 3)
            plt.bar(result_dir, np.mean(aggregated_rewards), label=f"{os.path.basename(result_dir)}")
            plt.xlabel("Result Directory")
            plt.ylabel("Average Reward")
            plt.title("Average Reward Comparison")
            plt.grid(True)
            plt.legend()  

    plt.tight_layout()

    # 创建 report 文件夹并保存图片
    os.makedirs("report", exist_ok=True)
    # 将 result_dirs 拼接到文件名中
    result_dirs_str = "_".join([os.path.basename(d) for d in result_dirs])
    save_path = os.path.join("report", f"compare_results_{result_dirs_str}_{target_trace}.png")
    plt.savefig(save_path)
    print(f"Plot saved to {save_path}")

    plt.show()


if __name__ == "__main__":
    # 比较的结果文件夹列表
    result_dirs = [
        './results_5_5',
        './results_5_10',
        './results_5_15',
    ]
    # 设置目标 trace
    target_trace = "norway_car_1"
    compare_results(result_dirs, target_trace)