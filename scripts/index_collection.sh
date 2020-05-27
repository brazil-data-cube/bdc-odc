#!/bin/bash

usage(){
	echo "Usage: $(basename $0) collection_name dest_folder"
}


if [ "$#" -ne 2 ]; then
	usage
	exit 1
fi

script_path=$(dirname $(realpath "$0") )
collection_id=$1
dest_path=$2
collection_path="${dest_path}/${collection_id}"
dataset_path="${collection_path}/datasets"

if [ ! -d $dest_path ]; then
	echo "$dest_path not found."
	exit 1
fi

mkdir -p $dataset_path

if [ ! -d $dataset_path ]; then
	echo "Was not possible to create $dataset_path"
	exit 1
fi

echo "Criando metadados do produto ${collection_id}"
python3 ${script_path}/collection2yaml/collection2yaml.py -c ${collection_id} -o ${collection_path}/${collection_id}.yaml

echo "Cadastrando produto"
#datacube product add ${collection_path}/${collection_id}.yaml

echo "Extraindo metadados dos itens (datasets)"
python3 ${script_path}/item2dataset/item2dataset.py -c ${collection_id} -o ${dataset_path}/

echo "Indexando datasets"
#find ${dataset_path}/*.yaml -exec datacube -vvv dataset add -p ${collection_id} {} \;



