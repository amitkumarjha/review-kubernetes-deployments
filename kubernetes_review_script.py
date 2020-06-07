#!/usr/bin/python3

import sys
import os
from yamllint.config import YamlLintConfig
from yamllint import linter
import yaml
import json
from collections import namedtuple

def verify_yaml(template_path):
    conf = YamlLintConfig('extends: default')
    f = open(template_path)
    gen = linter.run(f, conf)
    errors = list(gen)
    if errors:
        for error in errors:
            print(str(error))
        return False
    else:
        return True

def search_regex_nested_key(template_path,template_key,template_value):
    template_key = "x." + template_key
    data = []
    for keys in template_key.split("[*]"):
        new_data_main = []
        if data:
            for i in data:
                new_keys = str(i) + str(keys)
                dict = yaml.load_all(open(template_path))
                for dict_list in dict:
                    x = json.loads(json.dumps(dict_list), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
                    try:
                        if type(eval(new_keys)) is list:
                            length = len(eval(new_keys))
                            for i in range(length):
                                new_data = new_keys + "[" + str(i) + "]"
                                new_data_main.append(new_data)
                        else:
                            new_data = new_keys
                            new_data_main.append(new_data)
                    except AttributeError:
                        pass
            if new_data_main:
                data = new_data_main
            else:
                new_data = new_keys
                new_data_main.append(new_data)
                data = new_data_main
        else:
            dict = yaml.load_all(open(template_path))
            for dict_list in dict:
                x = json.loads(json.dumps(dict_list), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
                try:
                    length = len(eval(keys))
                    for i in range(length):
                        new_data = keys + "[" + str(i) + "]"
                        data.append(new_data)
                except AttributeError:
                    pass
                except IndexError:
                    pass
    for i in data:
        dict = yaml.load_all(open(template_path))
        for dict_list in dict:
            x = json.loads(json.dumps(dict_list), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            try:
                data_f = eval(i)
                if str(data_f) == str(template_value):
                    print("key = " + str(i.split("x.")[1]) + ", value = " + str(data_f) + ", " + template_path)
            except AttributeError:
                pass
            except IndexError:
                pass

def search_simple_nested_key(template_path, template_key, template_value):
    template_key = "x." + template_key
    dict = yaml.load_all(open(template_path))
    for dict_list in dict:
        x = json.loads(json.dumps(dict_list), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        try:
            data_f = eval(template_key)
            if str(data_f) == str(template_value):
                 print("key = " + str(template_key.split("x.")[1]) + ", value = " + str(data_f) + ", " + template_path)
        except AttributeError:
            pass
        except IndexError:
            pass

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Error: No arguments has been Given, Atleast 3 arguments needed to run the program")
        sys.exit(1)
    if len(sys.argv) < 4:
        print("Error: Not all arguments has been Passed, Atleast 3 arguments needed to run the program")
        sys.exit(1)
    if len(sys.argv) > 4:
        print("Error: More then 3 arguments has been Passed, Only 3 arguments needed to run the program")
        sys.exit(1)
    template_path = sys.argv[1]
    template_key = sys.argv[2]
    template_value = sys.argv[3]
    if os.path.isfile(template_path):
        verify_yaml(template_path)
        if "[*]" in template_key:
            search_regex_nested_key(template_path,template_key,template_value)
        else:
            search_simple_nested_key(template_path, template_key, template_value)
    if os.path.isdir(template_path):
        for root, dirs, files in os.walk(template_path):
            for file in files:
                if file.endswith(".yaml"):
                    verify_yaml(os.path.join(root, file))
                    if "[*]" in template_key:
                        search_regex_nested_key(os.path.join(root, file),template_key,template_value)
                    else:
                        search_simple_nested_key(os.path.join(root, file),template_key,template_value)