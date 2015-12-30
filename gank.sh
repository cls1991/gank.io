#!/bin/bash

:<<!
ReadMe:
自动运行gank
1. 键入source ./gank.sh运行该脚本
2. git pull更新
3. 激活python环境, 执行python脚本
4. wget执行下载任务
5. 检查本地是否有更改, 如果有, 推送到远程仓库
!

# 项目的python环境
virtual_python_dev="env_gank_io_2.7.6"
# 项目的根路径
project_dir="/home/taozhengkai/mygit/gank.io"
# 目标文件
result_file=gank.txt
pyenv activate $virtual_python_dev
cd $project_dir
# step 1: git pull更新
git pull
# step 2: 执行python脚本
python main.py
source deactivate
# step 3: wget执行下载
cd ./out
wget --no-clobber -i $result_file 
# step 4: 判断本地是否有更改
# 检查本地是否有改动需要提交
if git diff-index --quiet HEAD --; then
    # no changes
    :
else
    # changes
    git add $result_file
    comment="更新gank.txt"
    # 是否输入参数
    if [ ! -n "(" ] ;then
        :
    else
        # 获取外部参数
        getopts "m:" arg
        case $arg in
            m)
                comment=$OPTARG
                ;;
            ?)
                echo "unkonw argument"
                exit 1
                ;;
        esac
    fi

    git commit -m $comment

    # git push
    git push
fi
cd ..
