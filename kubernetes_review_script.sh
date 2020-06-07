#!/bin/bash

#List yaml files in a directory
list_all_yml_file(){
  files=$(find $1 -type f -name '*.yaml')
}

#Get values from the yaml for the key
get_key_value(){
  value=$(/usr/bin/yq r -d'*' $1 $2 )
  r_value=$(echo $value | sed 's/ -//g' | sed 's/- //g')
}

#Print the Data
print_data(){
      value=""
      get_key_value $1 $2
      if [ -z "$r_value" ]
      then
        continue
      else
        for j in $r_value
        do
          if [ "$j" == "null" ]
          then
            continue
          else
            if [ "$j" == "$template_value" ]
            then
              echo "Key = $2, value = $j, $1"
            else
              continue
            fi
          fi
        done
      fi
}

template_path=$1
template_key=$2
template_value=$3
if [ "$#" == "3" ]
then
  if [ -f "$template_path" ]; then
      print_data $1 $2
  elif [ -d "$template_path" ]; then
      list_all_yml_file "$template_path"
      if [ -z "$files" ]
      then
        echo "No yaml files found in Directory"
        exit
      fi
      for i in $files
      do
        print_data $i $2
      done
  else
      echo "file OR Directory is missing or does not exist"
  fi
else
  echo "Error: Not all arguments has been Passed, Only 3 arguments needed to run the program"
fi