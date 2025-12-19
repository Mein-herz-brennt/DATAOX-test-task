from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tasks.job import daily_job
scheduler = AsyncIOScheduler()
scheduler.add_job(daily_job, trigger="interval", days=1)
scheduler.start()
