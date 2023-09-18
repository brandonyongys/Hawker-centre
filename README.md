# SG Hawker Centre Dashboard

The Singapore Hawker Dashboard is developed using the data obtained from data.gov.sg via API endpoint. The data is then visualized using `plotly` and `folium` and it may be found here: [link](http://3.0.104.136/)

Via the dashboard, you would be able to have an overview of the current status of all hawker centres across Singapore. Besides that, you are able to hover over the hawker centre in the `folium` map or data table to find out more such as the closure dates etc.

Feel free to read more about the dashboard development in my [github.io](https://brandonyongys.github.io/) site. The specific posts are [here](https://brandonyongys.github.io/projects/2023-09-Hawker-centre-dashboard/) and [here](https://brandonyongys.github.io/blog/2023/Hawker-centre-dashboard/).

# Installation
1. All the required packages are in the `requirements.txt` and the source codes are within the `/src` folder.
1. There is no worries about the dependencies, prerequisites or system requirements as the dashboard would run in a Docker container.
1. The instructions to build and run the Docker image is as indicated in the [Usage](#usage) section.

# Usage
The dashboard may run locally on your machine by building and running the Docker image.
1. In a terminal, run the command `docker build -t hawker .` to build the Docker image.
1. After that, run the command `docker run -it -p 80:80 --name hawker hawker` to run the Docker image.
1. Navigate to `localhost:80` in your internet browser to interact with the dashboard. 

# License

This project is licensed under the [MIT License](LICENSE).

# Credits

I would like to say thank you to the authors:
* Benedict Soh for writing the wonderful [dengue dashboard post](https://towardsdatascience.com/creating-a-web-application-to-analyse-dengue-cases-1be4a708a533)
* Melvin Varughese for writing a post on [how to use Docker to deploy a Dashboard app on AWS](https://towardsdatascience.com/how-to-use-docker-to-deploy-a-dashboard-app-on-aws-8df5fb322708)

# Contact Information

If you have any feedback, feel free to reach out to me at byongys[at]gmail[dot]com