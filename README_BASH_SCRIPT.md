# Kubernetes config yaml review  bash script

##### The script parse the yaml deployment files and search for the key value pair in the yaml.


* ##### Installation

The script requires a third party tool **`jq`**. The script is written on top of the jq and act as a wrapper to
take arguments and pass it to the jq module. To run the script you need to install the `jq` on the machine and then
you can run the script. The script will automatically detect the  first argument as it is file or directory, if it 
is directory it will recursively parse and search the yamls files. 

[jq installation](http://mikefarah.github.io/yq/).

**NOTE: Below command only for ubunut18.04 LTS**
```
#sudo add-apt-repository ppa:rmescandon/yq
#sudo apt update
#sudo apt install yq -y
```

* ##### Usage

This script takes 3 arguments.

1) Path of the yaml **`File`** OR **`Directory`** where all the yaml files are placed.You can pass Either the full path of the
file or the Directory of the yaml files, the script will parse all the yaml files present on the Directory Recursively.

2) **`Key`** that need to searched in the yaml in the python object format. You can use any number of combination list 
or regex in the keys.

3) **`Value`** Value that need to be matched with the key passed as second argument.
 
* ##### Test Cases

#### File name with a simple key:
##### Input
```
# input file_name key value (this line is comment)
/bin/bash kubernetes_review_script.sh example-2.yaml kind Service
```
##### Output
```
key = kind, value = Service, example-2.yaml
```
#### File name with a nested list key with regex *:
##### Input
```
# input file_name key value (this line is comment)
/bin/bash kubernetes_review_script.sh example-2.yaml spec.template.spec.containers[*].ports[*].name http
```
##### Output
```
key = spec.template.spec.containers[*].ports[*].name, value = http, example-2.yaml
key = spec.template.spec.containers[*].ports[*].name, value = http, example-2.yaml
key = spec.template.spec.containers[*].ports[*].name, value = http, example-2.yaml

```

#### Directory with a nested list key with regex *:
##### Input
```
# input file_name key value (this line is comment)
/bin/bash kubernetes_review_script.sh templates/ spec.template.spec.containers[*].ports[*].name http
```
##### Output
```
key = spec.template.spec.containers[*].ports[*].name, value = http, templates/example-2.yaml
key = spec.template.spec.containers[*].ports[*].name, value = http, templates/example-1.yaml
key = spec.template.spec.containers[*].ports[*].name, value = http, templates/templates1/example-1.yaml
key = spec.template.spec.containers[*].ports[*].name, value = http, templates/templates1/templates2/example-2.yaml
key = spec.template.spec.containers[*].ports[*].name, value = http, templates/templates1/templates2/example-2.yaml
key = spec.template.spec.containers[*].ports[*].name, value = http, templates/templates1/templates2/example-2.yaml
key = spec.template.spec.containers[*].ports[*].name, value = http, templates/templates1/templates2/example-1.yaml

```

#### Directory with a nested list key with exact list element:
##### Input
```
# input file_name key value (this line is comment)
/bin/bash kubernetes_review_script.sh templates/ spec.template.spec.containers[1].ports[0].name http
```
##### Output
```
key = spec.template.spec.containers[1].ports[0].name, value = http, templates/templates1/templates2/example-2.yaml
```

#### Directory with a nested key:
##### Input
```
# input file_name key value (this line is comment)
/bin/bash kubernetes_review_script.sh templates/  spec.template.metadata.labels.app example-1
```
##### Output
```
key = spec.template.metadata.labels.app, value = example-1, templates/example-2.yaml
key = spec.template.metadata.labels.app, value = example-1, templates/example-1.yaml
key = spec.template.metadata.labels.app, value = example-1, templates/templates1/example-1.yaml
key = spec.template.metadata.labels.app, value = example-1, templates/templates1/templates2/example-2.yaml
key = spec.template.metadata.labels.app, value = example-1, templates/templates1/templates2/example-1.yaml

```
##### NOTE: There is one  minor bug is that in caes of regex [*] it wont print the  key correctly, but that not affecting the functionality of the script. The Python script does not have any issue yet identified.
[Python Script](README_PYTHON_SCRIPT.md) 
