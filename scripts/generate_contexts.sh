#!/bin/bash
#
#  Command Line Interface to start all services associated with the Tutorial
#  For this tutorial the commands are merely a convenience script to run docker or docker-compose
#
#  Each services script can be run using either docker-compose (the external tool with the hyphen -)
#  or docker compose (the newer version directly bundled with Docker with a space )
#
#  if you start up with the following command:
#
#  ./services start legacy
#
# This will force the script to use docker-compose which may be more reliable in
# some cases (or if an older version of Docker is being used)

set -e

if (($# < 1)); then
	echo "Illegal number of parameters"
	echo "usage: services [create|markdown|ngsi|jsonld|validate]"
	exit 1
fi

command="$1"
file="datamodels/airquality.yaml"
if (($# == 2)); then
	file="$2"
fi

case "${command}" in
"help")
	echo "usage: services [create|markdown|ngsi|jsonld|validate]"
	;;
"create")
	export $(cat .env | grep "#" -v)
	export $(cat .env | grep "#" -v)
	docker build -t contextgen ./ld-context-files
	;;
"markdown")
	echo "Creating Documentation for the Data Models"
	docker run --rm -v $(pwd)/:/files contextgen markdown -i "/files/${file}" >datamodels.md
	echo "datamodels.md created"
	;;
"ngsi")
	echo "Creating a NGSI-LD @context file for normalized interactions"
	docker run --rm -v $(pwd)/:/files contextgen ngsi -i "/files/${file}" >datamodels.context-ngsi.jsonld
	echo "datamodels.context-ngsi.jsonld created"
	;;
"jsonld")
	echo "Creating a JSON-LD @context file for key-values interactions"
	docker run --rm -v $(pwd)/:/files contextgen jsonld -i "/files/${file}" >datamodels.context.jsonld
	echo "datamodels.context.jsonld created"
	;;
"validate")
	docker run --rm -v $(pwd)/:/files contextgen validate -i "/files/${file}"
	;;
"start")
	export $(cat .env | grep "#" -v)
	./services ngsi $2
	;;
"stop")
	export $(cat .env | grep "#" -v)
	echo "no services running."
	;;
*)
	echo "Command not Found."
	echo "usage: services [create|markdown|ngsi|jsonld|validate]"
	exit 127
	;;
esac
