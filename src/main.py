import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import git


# 获取当前程序的路径
def get_current_path(debug):
    if debug:
        current_path = r'E:\LearningFile\Python'        # 在这里指定工作目录
    else:
        current_path = os.getcwd()
    return current_path

# --------------------------------------- End --------------------------------------- #


# 获取指定路径下的文件夹
def get_folders(path, find_all=False):
    if find_all:
        folders = []
        for root, dirs, files in os.walk(path):
            for dir in dirs:
                folders.append(os.path.relpath(os.path.join(root, dir), path))
    else:
        folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    return folders

# --------------------------------------- End --------------------------------------- #


# 获取文件夹下的所有 git 分支
def get_git_branches(folder_path):
    try:
        repo = git.Repo(folder_path)
        branches = [str(b) for b in repo.branches]
    except git.exc.InvalidGitRepositoryError:
        return None

    return branches

# --------------------------------------- End --------------------------------------- #


# 获取文件夹下的当前 git 分支
def get_current_git_branch(folder_path):
    try:
        repo = git.Repo(folder_path)
        branch = str(repo.active_branch)
    except git.exc.InvalidGitRepositoryError:
        return None
    return branch

# --------------------------------------- End --------------------------------------- #


def home_page(lst):
    # 创建主窗口
    root = tk.Tk()
    root.title("GitTool")

    # 创建左侧窗格
    left_frame = ttk.Frame(root, width=200, height=500)
    left_frame.pack(side="left")

    # 创建右侧窗格
    right_frame = ttk.Frame(root, width=250, height=500)
    right_frame.pack(side="right")

    # 创建分割线
    separator = ttk.Separator(root, orient="vertical")
    separator.pack(side="left", fill="y", padx=5)

    # 创建 Canvas 组件
    canvas = tk.Canvas(right_frame, width=240, height=500)
    canvas.pack(side="left", fill="both", expand=True)

    # 创建 Scrollbar 组件
    scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # 将 Scrollbar 组件与 Canvas 组件关联
    canvas.configure(yscrollcommand=scrollbar.set)

    # 创建 Frame 组件
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    # 用于存储选中的列表项
    selected_items = []

    # 复选框单击事件的回调函数
    def on_checkbox_click(checkbox_value, checkbox_state):
        if checkbox_state.get() == 1:
            selected_items.append(checkbox_value)
        else:
            selected_items.remove(checkbox_value)

    # 确定按钮单击事件的回调函数
    def on_ok_button_click():
        for widget in frame.winfo_children():
            widget.destroy()

        max_line = 40
        for folder in selected_items:
            label_right = tk.Label(frame, text=str(folder)+" 所有分支:")
            label_right.pack(padx=20)
            branch_list = get_git_branches(folder)
            if branch_list is not None:
                label_branch = tk.Label(frame, text="\n".join(branch_list))
                label_branch.pack(padx=20)
            else:
                label_branch = tk.Label(frame, text="None")
                label_branch.pack(padx=20)

            label_line = tk.Label(frame, text="-"*max_line)
            label_line.pack(padx=20)

    # 创建顶部标签
    label = tk.Label(left_frame, text="选择存储库")
    label.pack(side="top", padx=20, pady=10, anchor="center")

    # 创建复选框
    for i, item in enumerate(lst):
        checkbox_state = tk.IntVar()  # 用于记录每一个复选框的状态
        checkbox = tk.Checkbutton(left_frame, text=item, variable=checkbox_state, onvalue=1, offvalue=0,
                                  command=lambda value=item, state=checkbox_state: on_checkbox_click(value, state))
        checkbox.pack(side="top", padx=20, anchor="nw")

    # 创建确定按钮
    ok_button = tk.Button(left_frame, text="确定", command=on_ok_button_click)
    ok_button.pack()

    # 运行主循环
    root.mainloop()


# main
if __name__ == "__main__":
    is_debug = True         # 调试时, 请将该变量置为 True, 并在 get_current_path 函数中指定工作目录
    now_path = get_current_path(is_debug)

    # 获取当前路径下的所有一级文件夹
    folder_list = get_folders(now_path)

    # 开始运行函数
    home_page(folder_list)


