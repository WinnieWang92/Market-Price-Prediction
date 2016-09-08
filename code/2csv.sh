#!/usr/bin/env bash
file=$1
filename=`echo $file|awk -F . '{i=1;while(i<NF){ if(i==NF-1){printf $i} else{printf $i"."} i++}}'`
cat $1|awk -F \t '{i=1;while(i<=NF){if($i~/^[0-9]+([.]{1}[0-9]+){0,1}$/){ if(i==NF){printf("%.4f\n",$i)} else{printf("%.4f,",$i)}} else{ if(i==NF){printf $i"\n"} else{printf $i","}} i++}}' >$filename.csv

