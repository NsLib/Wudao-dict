#!/bin/bash

# 用户词
if [ ! -d usr ]
then
    mkdir usr
fi

chmod -R 777 usr

# 添加系统命令wd
echo '#!/bin/bash'>./wd
echo 'save_path=$PWD'>>./wd
echo 'cd '$PWD >>./wd
echo './wdd $*'>>./wd
echo 'cd $save_path'>>./wd
sudo cp ./wd /usr/local/bin/wd
sudo chmod +x /usr/local/bin/wd

echo 'Setup Finished! '
echo 'use wd [OPTION]... [WORD] to query the word.'

