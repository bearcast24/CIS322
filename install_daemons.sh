#!/bin/bash

#Kyile LeBlanc
#CIS 322
#Assigment 1
#install_daemons.sh



#The script will be invoked with an argument giving the install prefix 
#to be used when running the configure script for postgres and httpd.

install_prefix=$1

#clone the postgres source code from github

git clone https://github.com/postgres/postgres.git REL9_5_STABLE

cd REL9_5_STABLE

#configure/make/install postgres 9.5.x
./configure --prefix=$install_prefix
	
#To start the build
make

#Regression Tests
#make check

#install PostgreSQL
make install

# Move back to prefix
cd $install_prefix
##use curl to download Apache httpd-2.4.25

curl http://www.gtlib.gatech.edu/pub/apache//httpd/httpd-2.4.25.tar.bz2 > httpd-2.4.25.tar.bz2

tar -xjf httpd-2.4.25.tar.bz2

cd httpd-2.4.25

#configure/make/install httpd
./configure --prefix=$install_prefix

#To start the build
make
#install Apache httpd-2.4.25
make install 





