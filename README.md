# ONE TAP FASHIONISTA
### What is One Tap Fashionista? 
One Tap Fashionista is a project from four computer engineering students from Universitat Autònoma de Barcelona. Our project is part of Multimedia Systems' Hackaton of Google Cloud.

In this project we aim to build an application that is able to detect clothes in a photo and then change to any colour or a texture pattern.
The main idea is that every user with the app can upload or take photos and the edit it, like a fashion designer!

## Software achitecture

This is our software architecture scheme:

![image](https://user-images.githubusercontent.com/82968617/119484455-553f9700-bd56-11eb-9858-e7ead125156a.png)

When the photo is uploaded, the app's backend call the predictor hosted on the cloud server. The server returns a list of the predicted labels so the user can change the colors or patterns of the selected cloth piece.

After the user it's done with it, the backend sends a request to the server which applies the ModifyCloths function to realize the change. The server answers the request and the user gets the modified photo

## Mobile application



## Demonstration

## Authors
- Oriol Graupera Serra
- Josep Bravo Bravo
- Guillem Martínez Sánchez
- Arnau Revelles Segalés
