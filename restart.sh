#!/usr/bin/env bash

#Home_dir=$(cd "$(dirname "$0")"; pwd)
#cd $Home_dir
#mkdir -p tmp
#mkdir -p logs
#kill -quit `cat $Home_dir/tmp/gunicorn.pid`
#gunicorn data_catalogue.wsgi:application --bind 127.0.0.1:5001 --pid $Home_dir/tmp/gunicorn.pid -D
#echo success
#Home_dir=$(cd "$(dirname "$0")"; pwd)
#cd $Home_dir

#mkdir -p logs
#
#catalogue_port=5001
#
#if [ "${APP_ENV}" = "prod" ] ;
#then
#  killall -9 gunicorn
#  echo killall
#  gunicorn data_catalogue.wsgi:application -b 127.0.0.1:${catalogue_port} --pid /data/data_catalogue/tmp/gunicorn.pid --timeout 360 -w 4 -D
#  echo success
#else
#  kill -quit `cat $Home_dir/tmp/gunicorn.pid`
#  gunicorn data_catalogue.wsgi:application --bind 127.0.0.1:${catalogue_port} --pid $Home_dir/tmp/gunicorn.pid -D
#  echo success2
#fi
mkdir -p tmp
killall -9 gunicorn
echo killall
gunicorn yxdocking.wsgi:application -b 0.0.0.0:8770 --pid /data/quant/tmp/gunicorn.pid --timeout 360 -w 4 -D