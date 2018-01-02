#!/bin/bash

dir="/tmp/mongodbdata/`date +'%Y%m%d'`/"
db=$1
source=$2
target=$3
PORT=27017

echo "migrate <${db}> from <${source}> to <${target}>"

if [ ${source} == "a" ] && [ ${target} = "b" ]; then
    src_host=''
    dst_host=''
    src_psw=''
    dst_psw=''
elif [ ${source} = "b" ] && [ ${target} = "a" ]; then
    src_host=''
    dst_host=''
    src_psw=''
    dst_psw=''
else
    echo 'illegal parameter......'
    exit 1
fi

if [ ! -d ${dir} ]; then
    mkdir -p ${dir}
else
    cd ${dir}
    rm -rf *
fi

# mongodump
output=$(mongodump --host ${src_host} --port ${PORT} -u root -p ${src_psw} --authenticationDatabase admin -d ${db} --out ${dir} |& tail -1)
echo ${output}

if [[ ${output} == *"done dumping ${db}.coll"* ]]; then
    echo " "
    echo " "
    echo " "
    echo "mongodump done -----"
else
    echo " "
    echo " "
    echo " "
    echo "mongodump fail -----"
    exit 2
fi

sleep 2
echo 'Start to restore'

# mongorestore
mongorestore --host ${dst_host} --port ${PORT} -u root -p ${dst_psw} --authenticationDatabase admin ${dir}
