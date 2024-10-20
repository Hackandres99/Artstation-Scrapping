# Artstation Scraper
This program allow to get artist resume, artworks and artwork previews data of an artist on artstation 

To make sure this program works correctly on your machine, it is needed to follow the next steps:

## Installation
1. Download and install Python

    Ensure you have the last Python version installed. If not, download and install it from Python's official website. For detailed instructions, refer to the tutorials:
    - [Windows]
    - [Linux]
    - [macOs]
2. Clone or download the repository

    To clone the repository git has to be installed on your PC, for more info check this article: [How to install Git?]
3. Create a MongoDB atlas account

    In order to save the data to be extracted, it is necesary to have a mongo connection string, to know more, go to the next link: [Get Started with Atlas]
4. Create and activate a virtual environment

    Open a terminal in the downloaded folder and runs the following comands:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    or for Windows:
    ```sh
    python -m venv venv
    venv\Scripts\activate
    ```
5. Install the requiered packages:
    ```python
    pip install -r requirements.txt
    ```

## Configuration
1. Configure environment variables:

    Create a .env file in the root folder with the env vars on the MDB_Atlas/connection.py file, where each var represent:
    - **MONGODB_USERNAME**=the user name on your MongoDB Atlas account.
    - **MONGODB_PASSWORD**=the password on your MongoDB Atlas account.
    - **MONGODB_HOST**=the host on your MongoDB Atlas account.
    - **MONGODB_PORT**=the port configured to use on your MongoDB Atlas account, if this is not created the MongoDB default port will be added.
    - **MONGODB_DATABASE**=here the database could be created with your artist, business or the  name you need.
2. Configure execution flow:

    On the config.yaml file you could fill settings specifiying the artist or author name of which artworks and artwork previews will be acquired:

    **Here you can find the artist id, which is required for every action**
    ![artist id][artist_id]

    **Here you can find the artwork id, that each preview and artwork will have**
    ![artist id][artwork_id]

    **Number of previews and artworks**
    ![artworks and previews enumeration][artworks_previews]

    ### Actions:
    Depending the number you fill in action, the program will do one action or another:

    1. Get the artist data an save it in the artist mongoDB Atlas collection.

    2. Get the number of previews you desire to save in the preview mongoDB Atlas collection, if you type: 'all' in previews, this action will get all the previews that the artist has.

    3. Get the artwork identifier typed in artwork and save the data in the artwork mongoDB Atlas collection.

    4. Get the number of artworks you desire to save in the artwork mongoDB Atlas collection, if you type: 'all' in artworks, this action will get all the artworks that the artist has.

## Conclusion
This program is made to obtain the data of artworks loaded in the profile of an Artstation artist, in an easy and fast way, thanks to the Web-scrapping technique.

[windows]: https://www.geeksforgeeks.org/how-to-install-python-on-windows/

[Linux]: https://www.geeksforgeeks.org/how-to-install-python-on-linux/

[macOs]: https://www.geeksforgeeks.org/how-to-download-and-install-python-latest-version-on-macos-mac-os-x/

[How to install Git?]: https://kinsta.com/es/base-de-conocimiento/instalar-git/

[Get Started with Atlas]: https://www.mongodb.com/docs/atlas/getting-started/

[artist_id]: documentation/artist_id.jpg
[artwork_id]: documentation/artwork_id.jpg
[artworks_previews]: documentation/artworks_and_previews.jpg
