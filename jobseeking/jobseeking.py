from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import jobseeking.constants as const

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd


class Jobseeking(webdriver.Edge):
    def __init__(self) -> None:
        super(Jobseeking, self).__init__()
        self.implicitly_wait(5)
        self.maximize_window()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def get_job_content(self, job_link):
        data = {}
        data['link'] = job_link

        print("checking content....")

        WebDriverWait(self, 10).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    'div[data-automation="splitModeJobDetailsScrollWrapper"]'
                )
            )
        )

        details_title = self.find_element(
            by=By.CSS_SELECTOR,
            value='div[data-automation="detailsTitle"]'
        )
        data['title'] = details_title.find_element(
            by=By.CSS_SELECTOR,
            value='h1'
        ).text
        data['company'] = details_title.find_element(
            by=By.CSS_SELECTOR,
            value='span'
        ).text

        # ADDITIONALS DETAIL
        data['additional_title'] = self.find_element(
            by=By.XPATH,
            value='//div[@data-automation="jobDetailsHeader"]/div/div/div/div/div[2]'
        ).text.strip()

        # DESCRIPTION
        data['job_desc'] = self.find_element(
            by=By.XPATH,
            value='//div[@data-automation="jobDescription"]/span/div'
        ).text.strip()

        # INCLUDE KEYWORD
        include_keyword = []
        for key in const.INCLUDE_KEYWORDS:
            if key.lower() in data['job_desc'].lower():
                include_keyword.append(key)
            elif key.lower() in data['title'].lower():
                include_keyword.append(key)
        data['include_keyword'] = ','.join(
            include_keyword) if len(include_keyword) else '-'

        # EXCLUDE KEYWORD
        exclude_keyword = []
        for key in const.EXCLUDE_KEYWORDS:
            if key.lower() in data['job_desc'].lower():
                exclude_keyword.append(key)
            elif key.lower() in data['title'].lower():
                exclude_keyword.append(key)
        data['exclude_keyword'] = ','.join(
            exclude_keyword) if len(exclude_keyword) else '-'

        print(data['title'])
        return data

    def check_pagination(self):
        """
        return if success (str): "button"(not available), "a" (available) 
        """
        print("searching pagination...")
        try:
            # Locating pagination section on page
            pagination = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//div[@data-automation="pagination"]/*[3]'
                    )
                )
            )

            # scroll to pagination section
            self.execute_script(
                "arguments[0].scrollIntoView();", pagination)

            # store pagination tag name
            page_tag = pagination.tag_name

            # next page
            print(f"tag name:{page_tag}")

            pagination.click()

            return 1 if page_tag == "a" else 0
        except Exception as e:
            print(f"error: {e}")
            return 0

    def scroll_window(self, element):
        # scroll to the element
        self.execute_script(
            "arguments[0].scrollIntoView();",
            element
        )
        self.execute_script("window.scrollBy(0, -180);")

    def extract_jobs_page(self):
        # locating job listing div
        jobs_section = WebDriverWait(self, 30).until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    'div[data-automation="jobListing"]'
                )
            )
        )

        # locating each job title inside job listing
        jobs = jobs_section.find_elements(
            by=By.CSS_SELECTOR,
            value='h1'
        )
        print(f"result in current page:{len(jobs)}")

        job_df = pd.DataFrame()
        
        # extract each job
        for job in jobs:
            try:
                job_display = job.find_element(
                    by=By.CSS_SELECTOR,
                    value="a"
                )

                job_link = job_display.get_attribute("href")

                # scroll window
                self.scroll_window(job_display)

                # click job to open description
                job_display.click()

                job_content = self.get_job_content(job_link)
                new_df = pd.DataFrame([job_content])  # Dict to DF
                if job_df.empty:
                    job_df = pd.DataFrame(
                        columns=job_content.keys()
                    )

                job_df = pd.concat(
                    [job_df, new_df],
                    axis=0,
                    ignore_index=True
                )

            except Exception as e:
                print(f"error: {e}")
                pass

        return job_df
