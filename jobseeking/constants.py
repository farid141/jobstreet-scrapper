import time
# pastikan telah diurut dengan benar
# BASE_URL = "https://www.jobstreet.co.id/id/jobs?createdAt=14d&specialization=508%2C186&sort=createdAt"
BASE_URL = "https://www.jobstreet.co.id/id/python-jobs/in-Bandung-Jawa-Barat?specialization=508%2C186?createdAt=3d"
INCLUDE_KEYWORDS = ["python", "selenium", "microcontroller",
                    "arduino", "stm32", "esp32", "sensor", "iot", "excel", "sql", "analyst", "trainee", "wfh", "remote", "intern", "firmware", "embedded"]
EXCLUDE_KEYWORDS = ["fullstack", "android", "ios",
                    "flutter", "fiber", "full-stack", "full stack"]
FILE_OUT = f'result_jobstreet-{time.ctime().replace(":","-")}.csv'

# # surabaya tech
# BASE_URL = "https://www.jobstreet.co.id/id/jobs/in-Surabaya-Jawa-Timur?specialization=508%2C186"
# INCLUDE_KEYWORDS = ["python", "selenium", "microcontroller",
#                     "arduino", "stm32", "esp32", "sensor", "iot", "excel", "sql", "analyst", "trainee"]
# EXCLUDE_KEYWORDS = ["fullstack", "android", "ios", "flutter", "fiber"]