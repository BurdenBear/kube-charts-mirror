#!/usr/bin/env bash

repo=$GIT_REPO
interval=${UPDATE_INTERVAL:-86400}
root=/mnt/charts

mkdir -p $root

function init(){
cd $root
if [ ! -d ".git" ]; then
  git init
fi
git remote remove origin
git remote add origin $repo
git pull origin master
}

function update(){
mkdir -p $root/docs
cd ~
echo #### Begin to update mirror ####
python fetch.py
echo #### mirror update complete ####
date="`date '+%Y-%m-%d %H:%M:%S'`"
cd $root 
git add --all
git commit -a -m "update $date"
git push -u origin master
}

init
while true; do
update
sleep $interval
done
