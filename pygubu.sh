designer_dir="../pygubu-designer"

[[ -d $designer_dir ]] \
&& designer_dir_exist=t \
|| designer_dir_exist=f
dde=$designer_dir_exist

[[ $dde == t ]] && [[ -x $(which cmp)  ]] && \
cmp -s \
    "${designer_dir}/pygubudesigner/i18n.py" \
    "./pygubu/i18n.py" || \
cp ${designer_dir}/pygubudesigner/i18n.py ./pygubu/

project_dir_path="pygubu"
[[ $dde == t ]] && . ${designer_dir}/pygubudesigner.sh

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