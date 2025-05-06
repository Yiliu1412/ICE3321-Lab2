import importlib
import pkg_resources

def check_required_packages():
    """检查所需的 Python 包是否已安装，并输出版本号"""
    required_packages = ["matplotlib", "numpy"]
    all_installed = True

    for package in required_packages:
        try:
            module = importlib.import_module(package)
            version = pkg_resources.get_distribution(package).version
            print(f"{package} 已安装，版本: {version}")
        except ImportError:
            print(f" 缺少依赖包: {package}")
            all_installed = False
        except pkg_resources.DistributionNotFound:
            print(f"无法获取 {package} 的版本信息，但包已安装")
    
    return all_installed

def main():
    print("开始检查所需库...\n")
    packages_ok = check_required_packages()

    if packages_ok:
        print("\n 所有依赖库已安装！")
    else:
        print("\n 请安装缺少的依赖库后重试。")

if __name__ == "__main__":
    main()