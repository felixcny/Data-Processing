from dagster import ScheduleDefinition, DefaultScheduleStatus

planning_jour = ScheduleDefinition(
    name="planning_jour",
    job_name="job_complet_quotidien",
    cron_schedule="0 0 * * *", 
    execution_timezone="Europe/Paris",
    default_status=DefaultScheduleStatus.RUNNING
)
