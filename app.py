import streamlit as st
import asyncio
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters, \
    OnSiteOrRemoteFilters, SalaryBaseFilters

RESULTS_PER_PAGE = 3
#PAGINATION_SIZE = 25 # See AuthenticatedStrategy in LinkedinScraper

##### TODO: Improve the strategy for loading the jobs as quick as possible (for better UX)
# A nice strategy for loading fast the results could be to 
# # Load first 10 (which doesnt take too long)
# # Then in background load the remaining 15 thus all first 25 together
# # Then show the first 25 when the user clicks on more
# # # Then in the background already scrape 25 more

st.set_page_config(
    page_title="LinkedIn Job Scraper",
    layout="wide",
)

st.title("LinkedIn Job Scraper")

job_board = st.empty()

options = {}

# Sidebar inputs
with st.sidebar:
    options["job_title"] = st.text_input("Job Title", value="Data Scientist")
    options["location"] = st.text_input("Location", value="Sweden")
    # options["limit"] = st.number_input("Show", value=10, step=5)

    options["relevance"] = st.selectbox(
        'Sorting',
        ['Most Relevant', 'Most Recent']  
    )
    options["time"] = st.selectbox(
        'Select Time Filter',
        ['Anytime', 'Past 24 hours', 'Past Week', 'Past Month']  
    )
    options["type_filter"] = st.multiselect(
        'Select Job Type',
        ['Full-Time', 'Internship', 'Part-Time', 'Contract']  
    )
    options["on_site_or_remote"] = st.multiselect(
        'Select Work Type',
        ['On-Site', 'Remote', 'Hybrid'],
    )
    options["experience"] = st.multiselect(
        'Select Experience Level',
        ['Internship', 'Entry-Level', 'Mid-Senior'],
        default= ['Internship', 'Entry-Level']
    )

    search = st.button("Search")

# To store retrieved job data
jobs = []

# Event listener for LinkedIn jobs data
def on_data(data: EventData):
    job_info = {
        'title': data.title,
        'company': data.company,
        'company_link': data.company_link,
        'date': data.date,
        'link': data.link,
        'insights': data.insights,
        'description': data.description
    }
    jobs.append(job_info)
    # Update job data in Streamlit

# Initialize LinkedIn scraper
scraper = LinkedinScraper(
    chrome_executable_path=None,
    chrome_binary_location=None,
    chrome_options=None,
    headless=True,
    max_workers=1,
    slow_mo=0.5,
    page_load_timeout=40
)

# Add event listener for job data
scraper.on(Events.DATA, on_data)

async def gather_scrapes(currently_showing):
    print(options)
    queries = [
        Query(
            query='Data Scientist',
            options=QueryOptions(
                locations=['Sweden'],
                apply_link=True,  # Try to extract apply link (easy applies are skipped). If set to True, scraping is slower because an additional page must be navigated. Default to False.
                skip_promoted_jobs=False,  # Skip promoted jobs. Default to False.
                limit=currently_showing + RESULTS_PER_PAGE,
                page_offset=0,
                filters=QueryFilters(
                    relevance=RelevanceFilters.RELEVANT,
                    time=TimeFilters.WEEK,
                    type=[TypeFilters.FULL_TIME, TypeFilters.INTERNSHIP],
                )
            )
        ),
    ]
        
    await asyncio.to_thread(scraper.run, queries)

# To run async function in the background
async def scrape_jobs(currently_showing):    
    await asyncio.gather(gather_scrapes(currently_showing))

if search:
    if options["job_title"] == "":
        st.warning("Please enter a job title")
    elif options["location"] == "":
        st.warning("Please enter a location")
    else:

        jobs.clear()  # Clear previous job results

        if "jobs" in st.session_state:
            currently_showing = len(st.session_state.jobs)
        else:
            currently_showing = 0

        with st.spinner('Fetching results, please wait this could take a while...'):
            asyncio.run(scrape_jobs(currently_showing))

        # if "jobs" not in st.session_state:
        #     st.session_state.jobs = jobs
        # else:
        #     st.session_state.jobs += jobs
        st.session_state.jobs = jobs


if "jobs" in st.session_state:
    
    st.write(f'Currently showing {len(st.session_state.jobs)} jobs')

    for index, job in enumerate(st.session_state.jobs):
        # Create a container for each job ad
        with st.container():
            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(f"#### [{job['title']}]({job['link']})")  
                # Split the company string and format
                company_info = job['company'].split(' · ')
                if len(company_info) == 2:
                    company_name = company_info[0]
                    location_info = company_info[1]
                    st.write(f"**[{company_name}]({job['company_link']})** · {location_info}")
                else:
                    st.write(f"**[{job['company']}]({job['company_link']})**")  # Fallback in case of unexpected format

            with col2:
                st.button("Generate", key="button"+job['link'])
                st.write(index+1)
                

            # Full-width job description below in an expander
            with st.expander("...", expanded=False):
                st.write(job['description'])

                st.write("---")

                if job['insights']:  
                    st.write(f"- {job['insights'][0]}")  

            st.markdown("---")  
    
    if st.button("Load more"):
        if "jobs" in st.session_state:
            currently_showing = len(st.session_state.jobs)
        else:
            currently_showing = 0

        with st.spinner('Fetching more results, please wait...'):
            asyncio.run(scrape_jobs(currently_showing))

        st.session_state.jobs = jobs
        st.rerun() # Need to rerun otherwise it will show the old results


if "jobs" in st.session_state:
    print(len(st.session_state.jobs))