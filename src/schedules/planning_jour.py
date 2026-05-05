from dagster import ScheduleDefinition
from src.jobs.ingestions_job import chargement_tables_job

# planification tous les jours a minuit
planning_jour = ScheduleDefinition(
    job=chargement_tables_job,
    cron_schedule="0 0 * * *", 
    execution_timezone="Europe/Paris"
)
