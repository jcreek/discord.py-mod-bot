# discord.py-mod-bot

A simple bot that can be used to warn and semi-ban users of a discord server, sending sending a specific user (owner) a private message and adding the user who used a banned word to a specific role, posting in the channel what it has done.

**Update November 2019** - Now set up as a docker container to ensure full compatibility as I will not be maintaining this. Specific versions of Python and Discord.py are required for this script to work.

## How to install the mod-bot as a docker container on a server (raspberrypi)

### Building the image

Copy the folder containing the Dockerfile onto the server. Go to the directory that has the Dockerfile and run the following command to build the Docker image from the source code:

`docker build -t mod-bot .`

The image will now be listed by Docker. You can confirm this by running:

`docker images`

### Create a writeable container from the image

`docker create --name mod-bot mod-bot`

### Run the image

`docker start mod-bot`

### Set up a cronjob

Run the command below to edit the cronjobs:

`crontab -e`

Then add the below line to it:

`*/30 * * * * docker stop mod-bot && docker start mod-bot`

This will run the service every thirty minutes. To change this use [Crontab Guru](https://crontab.guru)

### View logs from inside the container

Run the below command to see the output of the bot.

`docker container logs -f mod-bot`
