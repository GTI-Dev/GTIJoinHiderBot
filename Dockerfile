FROM cyberuserbot/cyberspaceaz:dev
RUN git clone https://github.com/GettechinfoMA/GTIJoinHiderBot.git /root/GTIJoinHiderBot
WORKDIR /root/GTIJoinHiderBot/
RUN pip3 install -r requirements.txt
CMD ["python3", "bot.py"]
