FROM python:3.6.9

ADD mod-bot.py /
ADD swearWords.txt /

RUN pip install discord.py==0.16.12

CMD [ "python", "./mod-bot.py" ]