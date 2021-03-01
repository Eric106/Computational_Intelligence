# -*- coding: utf-8 -*-
from os import system
from datetime import datetime


def run_server():
    try:
        # system("git pull origin master")
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        gitUpdate(dt_string)
    except Exception as e:
        print(e)
        exit()
def gitUpdate(dt_string):
    system('git init')
    system('git add *')
    system('git commit -m '+'"'+dt_string+'"')
    system("git remote add origin https://github.com/Eric106/Computational_Intelligence.git")
    system('git push origin main')
run_server()
