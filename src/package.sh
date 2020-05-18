#!/bin/bash
delete(){
    for file in `ls -a $1`
    do
        if [ -d $1"/"$file ]
        then
            if [[ $file != '.' && $file != '..' ]]
            then
                delete $1"/"$file
            fi
        else
            echo 删除 $1"/"$file
            rm -rf $1"/"$file
        fi
    done
    echo 删除 $1
    rm -rf $1
}
delete \build
delete \dist

echo 删除 *.spec
rm -rf *.spec

echo 开始打包 ...
pyinstaller -D -F application.py -w

echo 复制资源文件 ...
cp -rvf config dist/config
cp -rvf resources dist/resources
echo 打包完成