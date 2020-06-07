# Kubernetes config yaml review script

##### The script parse the yaml deployment files, check for lint error in yml and search for the key value pair in the yaml.


* ##### Installation

The script requires atleast python3.6. So before running the script please make sure you have a valid python
3.6 version installed in the machine. You can also follow this links to configure/install python3.6 in the machine,
[Python installation](https://realpython.com/installing-python/).

Now install other packages required to run the script.

**NOTE: Below command only for ubunut18.04 LTS**
```
#apt-get update -y
#apt-get install python3-pip -y
#pip3 install yamllint
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
python3 kubernetes_review_script.py example-2.yaml kind Service
```
##### Output
```
key = kind, value = Service, example-2.yaml
```
#### File name with a nested list key with regex *:
##### Input
```
# input file_name key value (this line is comment)
python3 kubernetes_review_script.py example-2.yaml spec.template.spec.containers[*].ports[*].name http
```
##### Output
```
key = spec.template.spec.containers[0].ports[0].name, value = http, example-2.yaml
key = spec.template.spec.containers[1].ports[0].name, value = http, example-2.yaml
key = spec.template.spec.containers[1].ports[1].name, value = http, example-2.yaml

```

#### Directory with a nested list key with regex *:
##### Input
```
# input file_name key value (this line is comment)
python3 kubernetes_review_script.py templates/ spec.template.spec.containers[*].ports[*].name http
```
##### Output
```
key = spec.template.spec.containers[0].ports[0].name, value = http, templates/example-2.yaml
key = spec.template.spec.containers[0].ports[0].name, value = http, templates/example-1.yaml
key = spec.template.spec.containers[0].ports[0].name, value = http, templates/templates1/example-1.yaml
key = spec.template.spec.containers[0].ports[0].name, value = http, templates/templates1/templates2/example-2.yaml
key = spec.template.spec.containers[1].ports[0].name, value = http, templates/templates1/templates2/example-2.yaml
key = spec.template.spec.containers[1].ports[1].name, value = http, templates/templates1/templates2/example-2.yaml
key = spec.template.spec.containers[0].ports[0].name, value = http, templates/templates1/templates2/example-1.yaml

```

#### Directory with a nested list key with exact list element:
##### Input
```
# input file_name key value (this line is comment)
python3 kubernetes_review_script.py templates/ spec.template.spec.containers[1].ports[0].name http
```
##### Output
```
key = spec.template.spec.containers[1].ports[0].name, value = http, templates/templates1/templates2/example-2.yaml
```

#### Directory with a nested key:
##### Input
```
# input file_name key value (this line is comment)
python3 kubernetes_review_script.py templates/  spec.template.metadata.labels.app example-1
```
##### Output
```
key = spec.template.metadata.labels.app, value = example-1, templates/example-2.yaml
key = spec.template.metadata.labels.app, value = example-1, templates/example-1.yaml
key = spec.template.metadata.labels.app, value = example-1, templates/templates1/example-1.yaml
key = spec.template.metadata.labels.app, value = example-1, templates/templates1/templates2/example-2.yaml
key = spec.template.metadata.labels.app, value = example-1, templates/templates1/templates2/example-1.yaml

```
