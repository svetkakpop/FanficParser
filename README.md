# FanficParser
This code is designed to scrape fanfiction data from the Archive of Our Own (AO3) website. It allows users to search for fanfics based on specific criteria, including fandom, pairing, tags, and the number of kudos. The main functionalities of the code include:

# Fetching Fanfiction:

The fetch_fanfiction function constructs a search URL based on user-provided parameters and sends a request to the AO3 website. It retrieves the HTML content of the search results page.
The function extracts relevant information for each fanfic, including the title, author, link, and description. Note: The description functionality is currently unavailable but will be added soon.

Saving Information:
The save_to_txt function saves the extracted fanfic data into a text file named fanfics.txt, including the title, author, link, and description of each fanfic.
Downloading Content:

The download_fanfic function allows users to download the content of a specific fanfic by extracting text from a designated HTML element and saving it to a file named fanfic.txt.
Interactive User Interface:

The code includes a command-line interface that prompts users for the necessary search parameters and displays the results. Users can choose to download the content of a specific fanfic.

# How to Run the Code

Install Required Libraries: 
Make sure you have Python installed on your machine. You will also need to install the requests and BeautifulSoup4 libraries if you haven't already. You can install them using pip:
pip install requests beautifulsoup4

Run the Script: 
Open a terminal or command prompt, navigate to the directory where your Python file is located, and run the script using the following command:
python code.py
Input Parameters: When prompted, enter the fandom, pairing, tags, and maximum number of kudos you want to search for. 

# For example:
Enter fandom: Harry Potter

Enter pairing (format Name/Name): Harry/Draco

Enter tags separated by commas (e.g., Angst, Fluff): Fluff, Romance

Enter maximum number of kudos (kudos): 100

View Results: After the search is complete, the script will save the results in a file named fanfics.txt. If you choose to download a specific fanfic, its content will be saved in fanfic.txt.

By following these steps, you can effectively use the code to search for and download fanfiction from the Archive of Our Own website
