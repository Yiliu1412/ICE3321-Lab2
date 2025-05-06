import os
import matplotlib.pyplot as plt
import numpy as np

def parse_log_file(log_file_path):
    """解析日志文件，提取时间戳、码率、缓冲区大小、卡顿时间、质量波动和奖励"""
    time_stamps = []
    bit_rates = []
    rebuffer_times = []
    quality_variations = []
    rewards = []

    with open(log_file_path, 'r') as f:
        last_bit_rate = None
        for line in f:
            if line.strip():  # 跳过空行
                data = line.split('\t')
                time_stamps.append(float(data[0]))  # 时间戳
                bit_rates.append(float(data[1]))  # 码率
                rebuffer_times.append(float(data[3]))  # 卡顿时间
                rewards.append(float(data[6]))  # 奖励

                # 计算质量波动
                if last_bit_rate is not None:
                    quality_variations.append(abs(float(data[1]) - last_bit_rate))
                last_bit_rate = float(data[1])

    return time_stamps, bit_rates, rebuffer_times, quality_variations, rewards


def compare_bba_rb(result_dirs, target_trace):
    """比较 BBA 和 RB 算法的性能"""
    # 初始化指标
    metrics = {
        "bit_rates": [],
        "rebuffer_times": [],
        "quality_variations": [],
        "rewards": []
    }

    # 创建绘图数据
    plot_data = []

    for result_dir in result_dirs:
        # 适配不同算法生成的日志文件
        log_files = [os.path.join(result_dir, f) for f in os.listdir(result_dir) 
                     if (f.startswith('log_sim_bb') or f.startswith('log_sim_rb')) and f.endswith(f"_{target_trace}")]

        print(f"Checking directory: {result_dir}")
        print(f"Matched log files: {log_files}")

        if not log_files:
            print(f"No log files found in {result_dir} for trace {target_trace}")
            continue

        for log_file in log_files:
            print(f"Parsing log file: {log_file}")
            time_stamps, bit_rates, rebuffer_times, quality_variations, rewards = parse_log_file(log_file)

            if not time_stamps or not bit_rates or not rebuffer_times:
                print(f"No data to plot for {log_file}")
                continue

            # 计算平均指标
            metrics["bit_rates"].append(np.mean(bit_rates))
            metrics["rebuffer_times"].append(np.sum(rebuffer_times))  # 总卡顿时间
            metrics["quality_variations"].append(np.mean(quality_variations))
            metrics["rewards"].append(np.mean(rewards))

            # 保存绘图数据
            plot_data.append({
                "time_stamps": time_stamps,
                "bit_rates": bit_rates,
                "rebuffer_times": rebuffer_times,
                "quality_variations": quality_variations,
                "label": f"{os.path.basename(result_dir)} - {os.path.basename(log_file)}"
            })

    # 绘制第一张图：码率、卡顿时间、质量波动
    plt.figure(figsize=(15, 10))

    # 码率随时间变化
    plt.subplot(3, 1, 1)
    for data in plot_data:
        plt.plot(data["time_stamps"], data["bit_rates"], label=data["label"])
    plt.xlabel("Time (s)")
    plt.ylabel("Bitrate (Kbps)")
    plt.title("Bitrate over Time")
    plt.legend()
    plt.grid(True)

    # 卡顿时间随时间变化
    plt.subplot(3, 1, 2)
    for data in plot_data:
        plt.plot(data["time_stamps"], data["rebuffer_times"], label=data["label"])
    plt.xlabel("Time (s)")
    plt.ylabel("Rebuffer Time (s)")
    plt.title("Rebuffer Time over Time")
    plt.legend()
    plt.grid(True)

    # 质量波动随时间变化
    plt.subplot(3, 1, 3)
    for data in plot_data:
        plt.plot(data["time_stamps"][:-1], data["quality_variations"], label=data["label"])
    plt.xlabel("Time (s)")
    plt.ylabel("Quality Variation (Kbps)")
    plt.title("Quality Variation over Time")
    plt.legend()
    plt.grid(True)

    # 保存第一张图
    os.makedirs("report", exist_ok=True)
    save_path_1 = os.path.join("report", f"compare_bba_rb_{target_trace}_time_metrics.png")
    plt.tight_layout()
    plt.savefig(save_path_1)
    print(f"Time-based metrics plot saved to {save_path_1}")

    # 绘制第二张图：仅比较综合 QoE（Reward）
    plt.figure(figsize=(8, 6))
    x_labels = [os.path.basename(d) for d in result_dirs]
    x = np.arange(len(x_labels))
    bar_width = 0.4

    # 综合 QoE
    plt.bar(x, metrics["rewards"], bar_width, label="Average QoE (Reward)", color='b')

    plt.xticks(x, x_labels)
    plt.xlabel("Result Directory")
    plt.ylabel("Average QoE (Reward)")
    plt.title("Performance Comparison (Average QoE)")
    plt.legend()
    plt.grid(True)

    # 保存第二张图
    save_path_2 = os.path.join("report", f"compare_bba_rb_{target_trace}_reward_metrics.png")
    plt.tight_layout()
    plt.savefig(save_path_2)
    print(f"Reward metrics plot saved to {save_path_2}")

    plt.show()


if __name__ == "__main__":
    # 比较的结果文件夹列表
    result_dirs = [
        './results_5_10',
        './results_rb',
    ]
    # 设置目标 trace
    target_trace = "norway_ferry_1"
    compare_bba_rb(result_dirs, target_trace)