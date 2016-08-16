#!/bin/bash
# url: http://stackoverflow.com/questions/3510673/find-and-kill-a-process-in-one-line-using-bash-and-regex
kill $(ps -ef | grep $1 | grep nc | awk '{print $2}')
