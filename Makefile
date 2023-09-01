dup:
		docker-compose up -d --build --remove-orphans
duu:
		docker-compose up -d
ddo:
		docker-compose down
dps:
		docker-compose ps -a
dlo:
		docker-compose logs $(argument) -f
dba:
		docker exec -it postgres /bin/sh
dip:
		docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' postgres