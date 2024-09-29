# Streamlit LinkedIn Job Scraper 

> [!WARNING]
> **DISCLAIMER**: This application is intended for **personal or educational use only**. All the job data retrieved by using this tool is publicly available on the LinkedIn website and remains the property of LinkedIn. The creator of this Streamlit app is not responsible for any inappropriate or unauthorized use of the data extracted through this tool. Please comply with LinkedIn’s terms of service and avoid any misuse of the data.


Welcome to the **Streamlit** app for the [**Py LinkedIn Job Scraper**](https://github.com/spinlud/py-linkedin-jobs-scraper), a stateless app built with Streamlit that integrates the `linkedin-jobs-scraper` library for fetching and displaying LinkedIn job postings. With this tool, you can search for jobs, view key information, and use the retrieved data for any purpose, whether it's analyzing trends, saving listings, or exploring new opportunities.

## 🎯 Features

- **Job Search Customization**: Input a **job title**, **location**, and refine your search using filters like job type, experience level, and more.
- **Dynamic Pagination**: Load more jobs incrementally, optimizing both speed and user experience.
- **Versatile Data Usage**: You can scrape job data and use it however you like—whether for personal exploration, data analysis, or integration into other projects.

## 🚀 Installation & Setup

### Requirements

* **Python >=3.7**

### Step-by-Step Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/streamlit-linkedin-jobs.git
   cd streamlit-linkedin-jobs
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app**:
   ⚠ Set the environment variable `LI_AT_COOKIE` as [described in step 3](https://github.com/spinlud/py-linkedin-jobs-scraper#anonymous-vs-authenticated-session)
   ```bash
   LI_AT_COOKIE=<your-cookie-here> streamlit run app.py
   ```


## 🛠 Usage Guide

1. **Enter Job Search Details**: On the sidebar, provide the **job title** and **location** to start searching. You can also use filters like:
   - **Relevance**: Sort by relevance or most recent.
   - **Time Posted**: Filter jobs based on when they were posted (e.g., last 24 hours, past week).
   - **Job Type**: Full-time, part-time, contract, internship, etc.
   - **Work Type**: On-site, remote, or hybrid.
   - **Experience Level**: Entry-level, mid-senior, internship, etc.

2. **Start Search**: Click the **Search** button to begin scraping job postings from LinkedIn.

3. **View Results**: Job results will appear dynamically. Expand each job card to see:
   - **Job title** and **company link**.
   - **Job description** with insights (if available).
   - **Application link** to apply directly on LinkedIn.

4. **Load More Jobs**: Click the **Load More** button to fetch additional job listings without refreshing the page.

![App Screenshot](screenshot.png) <!-- TODO: Add a screenshot here -->

## 🔧 Customization

You can modify the app to suit your needs:

- **Scraping Filters**: Customize which filters are active by default in `app.py`.
- **Data Usage**: Since the job data is stored as Python objects, you can easily extend the functionality to:
  - Use LLMs for any post-processing
  - Export job listings to CSV or JSON.
  - Analyze trends in job postings.
  - Integrate the scraped data into your own applications.

## ⚠️ Important Notes

- **Stateless**: There is no user session, at each new session the data is flushed.
- **LinkedIn Rate Limits**: This app uses the `linkedin-jobs-scraper` library, which employs web scraping. LinkedIn may impose rate limits on scraping, so use it cautiously to avoid being blocked temporarily.
- **Headless Browser**: The scraper runs in a headless Chrome browser, which means you won't see the scraping process visually, but it operates in the background.

## 💡 Future Improvements

- **LLM Integration**: Integrate LLM analysis on job posts
- **Asynchronous Scraping**: Enhance job fetching speed by implementing asynchronous scraping.
- **User Preferences**: Allow users to save search preferences and reuse them later.
- **Export Functionality**: Add a feature to download the job data as CSV or JSON files for further use.
  
## 🤝 Contributing

I welcome contributions! If you have suggestions or find bugs, feel free to open an issue. You can also submit pull requests for improvements or new features.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Enjoy using the **LinkedIn Job Scraper** to supercharge your job search and data analysis! 🚀

Cheers
