#!/bin/bash

designer_dir="../pygubu-designer"

project_dir_path="pygubu"
[[ $dde == t ]] && . ${designer_dir}/devtool.sh

install_designer(){
    pip3 install -e $designer_dir
}

test_installation(){
    pip3 install -e .
    pip3 install -e $designer_dir
    pygubu-designer
}

insd(){     install_designer;   }
ti(){       test_installation;  }

$*
