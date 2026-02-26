# Launch MySQL In Docker

docker run -d -m "1g" -p 127.0.0.1:3306:3306 -e MYSQL_DATABASE=cs544 -e MYSQL_ROOT_PASSWORD=abc mysql
