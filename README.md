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

Lancer dbt tests : 
docker exec -it dagster_app dbt test --project-dir /opt/dagster/app/dbt_project --profiles-dir /opt/dagster/app/dbt_project


Lancer pytest:
docker exec -it dagster_app pytest /opt/dagster/app/tests

Si besoin: 
docker exec -it dagster_app pip install pytest

Snapshot :
docker exec -it dagster_app dbt snapshot --project-dir /opt/dagster/app/dbt_project --profiles-dir /opt/dagster/app/dbt_project

Lancer dbt docs:
docker exec -it dagster_app dbt docs serve --host 0.0.0.0 --port 8081 --project-dir /opt/dagster/app/dbt_project --profiles-dir /opt/dagster/app/dbt_project