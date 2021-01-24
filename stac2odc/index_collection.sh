#!/bin/bash

usage(){
	echo "Usage: $(basename $0) collection_name dest_folder units platform instrument maxelements"
}


if [ "$#" -ne 2 ]; then
	usage
	exit 1
fi

script_path=$(dirname $(realpath "$0") )
collection_id=$1
dest_path=$2
units=$3
platform=$4
instrument=$5
maxelements=$6
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

echo "Creating product metadata ${collection_id}"
stac2odc -c ${collection_id} -o ${collection_path}/${collection_id}.yaml --units ${units} -p ${platform} \ 
                                                                                    --instrument ${instrument} \
                                                                                    -m ${maxelements} 

echo "Registering a product"
datacube product add ${collection_path}/${collection_id}.yaml

echo "Extracting item metadata (datasets)"
stac2odc  -c ${collection_id} -o ${dataset_path}/ --units ${units} -p ${platform} \ 
                                                            --instrument ${instrument} \
                                                            -m ${maxelements} 

echo "Indexing datasets"
find ${dataset_path}/*.yaml -exec datacube -v dataset add -p ${collection_id} {} \;
