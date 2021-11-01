import re
from flask.helpers import make_response
from app.java.models_java import Challenge_java
from . import java
from app import db
import os
from flask import Flask, flash, request, redirect, url_for, jsonify, json
from werkzeug.utils import secure_filename
from json import loads
from types import TracebackType
import subprocess
import os.path
from subprocess import STDOUT, PIPE
from os import remove
from os import path

class controller():

    def list_challenges_java():
        challenge = {"challenges":[]}
        challenge ['challenges'] = Challenge_java.query.all()
        all_challenges=[]
        for i in challenge['challenges']:
            aux_challenge = Challenge_java.__repr__(i)
            nombre_code = aux_challenge['code']
            path='public/challenges/' + nombre_code + '.java'
            file = open (path,mode='r',encoding='utf-8')
            filemostrar=file.read()
            file.close()
            aux_challenge['code']=filemostrar
            aux_challenge.pop('tests_code',None)
            all_challenges.append(aux_challenge)
        return make_response(jsonify({"challenges":all_challenges}))