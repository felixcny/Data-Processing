#on peut détruire limage si il est en cours
docker-compose down --rmi all --volumes

#construire limage et le lancer
docker-compose up -d --build

#éxecuter mes jobs dagster et vérifier les tables dans duckdb

#installer les dépendances dbt
docker compose run --rm dbt dbt deps

#ensuite lancer dbt
docker compose run --rm dbt dbt run

#verifier nos tables staging, dimension ...etc