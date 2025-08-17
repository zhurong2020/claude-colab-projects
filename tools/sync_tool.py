#!/usr/bin/env python3
"""
Claude Code + Colab 快速同步工具
简化的项目同步和Colab链接生成
"""

import subprocess
import argparse
from pathlib import Path

def run_command(cmd, check=True):
    """运行命令并处理错误"""
    print(f"🔧 执行: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {e}")
        if e.stderr:
            print(f"错误信息: {e.stderr.strip()}")
        return False

def check_git_status():
    """检查Git状态"""
    print("📋 检查Git状态...")
    if not run_command("git status --porcelain", check=False):
        print("❌ 当前目录不是Git仓库")
        return False
    return True

def sync_to_github(message="Update from Claude Code"):
    """同步到GitHub"""
    if not check_git_status():
        return False
        
    print("📤 同步到GitHub...")
    
    commands = [
        "git add .",
        f'git commit -m "{message}"',
        "git push"
    ]
    
    for cmd in commands:
        if not run_command(cmd, check=False):
            if "git commit" in cmd:
                print("ℹ️ 没有需要提交的更改")
                continue
            return False
    
    print("✅ GitHub同步完成!")
    return True

def generate_colab_links(github_repo):
    """生成Colab链接"""
    base_url = f"https://colab.research.google.com/github/{github_repo}/blob/main"
    
    print(f"\n🔗 Colab链接生成 ({github_repo}):")
    
    # 查找所有notebook文件
    notebooks = list(Path.cwd().glob("**/*.ipynb"))
    
    if not notebooks:
        print("❌ 未找到notebook文件")
        return
    
    print("\n📓 可用的Colab链接:")
    for nb in notebooks:
        try:
            rel_path = nb.relative_to(Path.cwd())
            link = f"{base_url}/{rel_path}"
            print(f"   • {nb.name}: {link}")
        except ValueError:
            # 如果文件不在当前目录下
            continue

def quick_setup_git(github_repo):
    """快速设置Git远程仓库"""
    print("🔧 设置Git远程仓库...")
    
    # 检查是否已经设置了remote origin
    result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"ℹ️ 远程仓库已设置: {result.stdout.strip()}")
        return True
    
    # 设置远程仓库
    remote_url = f"https://github.com/{github_repo}.git"
    if run_command(f"git remote add origin {remote_url}"):
        print(f"✅ 远程仓库设置完成: {remote_url}")
        return True
    
    return False

def main():
    parser = argparse.ArgumentParser(description='Claude Code + Colab 快速同步工具')
    subparsers = parser.add_subparsers(dest='action', help='操作类型')
    
    # 同步命令
    sync_parser = subparsers.add_parser('sync', help='同步到GitHub')
    sync_parser.add_argument('--message', '-m', default="Update from Claude Code", help='提交信息')
    
    # 生成链接命令
    links_parser = subparsers.add_parser('links', help='生成Colab链接')
    links_parser.add_argument('github_repo', help='GitHub仓库 (username/repo)')
    
    # 完整流程命令
    full_parser = subparsers.add_parser('full', help='完整流程：同步 + 生成链接')
    full_parser.add_argument('github_repo', help='GitHub仓库 (username/repo)')
    full_parser.add_argument('--message', '-m', default="Update from Claude Code", help='提交信息')
    
    # 初始化命令
    init_parser = subparsers.add_parser('init', help='初始化Git仓库并设置远程')
    init_parser.add_argument('github_repo', help='GitHub仓库 (username/repo)')
    
    args = parser.parse_args()
    
    if args.action == 'sync':
        sync_to_github(args.message)
    
    elif args.action == 'links':
        generate_colab_links(args.github_repo)
    
    elif args.action == 'full':
        if sync_to_github(args.message):
            generate_colab_links(args.github_repo)
    
    elif args.action == 'init':
        # 初始化Git仓库
        if not Path('.git').exists():
            print("🔧 初始化Git仓库...")
            run_command("git init")
            run_command("git branch -M main")
        
        # 设置远程仓库
        quick_setup_git(args.github_repo)
        
        # 首次提交
        print("📤 进行首次提交...")
        run_command("git add .")
        run_command('git commit -m "Initial commit"')
        run_command("git push -u origin main")
        
        # 生成链接
        generate_colab_links(args.github_repo)
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()