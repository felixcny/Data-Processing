#reset des données du projet
docker compose down -v --remove-orphans \
&& docker system prune -a --volumes -f \
&& rm -rf target dbt_packages logs \
&& rm -rf dbt_project/*.duckdb \
&& dbt clean

#construire limage et le lancer
docker-compose up -d --build

#éxecuter mes jobs dagster et vérifier les tables dans duckdb

#si ce n'est pas fait créer la base
duckdb data/local_database.duckdb

#verifier nos tables staging, dimension ...etc

Lancer pytest:
docker exec -it dagster_app pytest /opt/dagster/app/tests

Snapshot :
docker exec -it dagster_app dbt snapshot --project-dir /opt/dagster/app/dbt_project --profiles-dir /opt/dagster/app/dbt_project

Lancer dbt docs:
#éxexuter la génération
docker exec -it dagster_app dbt docs generate --project-dir /opt/dagster/app/dbt_project --profiles-dir /opt/dagster/app/dbt_project

#
docker exec -it dagster_app dbt docs serve --host 0.0.0.0 --port 8081 --project-dir /opt/dagster/app/dbt_project --profiles-dir /opt/dagster/app/dbt_project