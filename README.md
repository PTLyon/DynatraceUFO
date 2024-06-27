# DynatraceUFO

This is a respository meant to hold scripts that facilitate or add functions to Dynatrace's UFO, a device for companies that face the challenges of a distributed team. The Dynatrace DevOps UFO is a highly visible IoT gadget to share the status of a project. Using our UFOs, a quick stroll through the office, or a glance to the other side of the room, can alert you to problems.

The issue I was faced with was that the UFO could only deal with Dynatrace's v1 API. So what I did was write a couple of scripts that would call the V2 Dynatrace API, translate and process the information, and then proceed to call the UFO's own API to change the lights accoding to the data received.

Currently, the repository contains 2 files:

- ### printProblems.py

  - This is a very simple script that takes advantage of Dynatrace v2 API and fetches all the current **open** problems from your Dynatrace Environment and pritns them to a file. I used this for testing purposes.
    
- ### UFOMonitorV4.py
  - This script is prepared to deal with 5 different environments at once. All you have to do is replace the token and environment placeholders, give it your UFO's IPaddr and it should work. It will light up five colors on the upper row of the UFO. Each color represents a different environment. Below, it will either not light up (if problems are below the defined treshold), light up yellow or light up red. This depends on the number of problems present in the environment and also the numbers you define on the treshold constants for each environment.
