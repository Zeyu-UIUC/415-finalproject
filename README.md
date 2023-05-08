# CS445 Final Project: Hand Gesture Recognition

Paper for reproduction: https://ieeexplore.ieee.org/document/8373818

# Instructions

1. Download the dataset from this [website](http://www-rech.telecom-lille.fr/shrec2017-hand/). <br>

2. Then, run LoadData.py to generate.pckl format data. <br>

3. To train the model, run main.ipynb <br>

4. To generate hand data sequences for prediction, purchase Leap motion camera and install the necessary tracking software and packages: [Leap Motion](https://developer.leapmotion.com/?_gl=1*1i38fke*_ga*MTA0MzE5MTQwNy4xNjc5MzQxNDEy*_ga_5G8B19JLWG*MTY4MzQ4MTA3OC4xNS4xLjE2ODM0ODEwODguNTAuMC4w). Then, Open unity project using unityFiles, run the application, and it will record the hand data for 100 frames. The output result will store in handgesture.csv file inside the unityFiles. The script for Collecting hand data can found in here: UnityFiles/Assets/getHandData.cs

5. To predict the gesture using data generated from unity, run the predcition code cell in main.ipynb.
    

# File organization
FinalProject: The folder containing all files related to the Model, including preprocessing data, training data, and gesture prediction. 
UnityFile: The folder for Unity Project. The script is stored in the Assets folder. The Leap motion Unity Package is imported. 
