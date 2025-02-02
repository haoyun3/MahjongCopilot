import subprocess


def run_interactive_program(name: str):
    """
    启动一个新的命令行窗口，激活指定的 Conda 环境，并运行交互式 Python 程序。

    """
    conda_env_name = "mahjong"
    # 构造命令
    command = rf"conda activate {conda_env_name} && python -i activity\{name}.py"

    # 使用 subprocess 启动新的命令行窗口并执行命令
    subprocess.Popen(["start", "cmd", "/k", command], shell=True)
