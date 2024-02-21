# Put me in, Coach!

![main image](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/002/776/157/datas/gallery.jpg)  
[![Watch the video](https://img.youtube.com/vi/D2bPI29tvSQ/default.jpg)](https://youtu.be/D2bPI29tvSQ)  

### Inspiration
Hiring an athletic trainer is expensive and logistically troublesome. But for our beloved friends who're insanely into playing sports, and our family who're aspiring to improve their performance, perhaps playing as a starter in a varsity team or simply challenging themselves, there is simply no other way than hiring an hourly-rating athletic trainer. We want to say goodbye to the hassle and expense and provide you with a more personalized, professional, and wholistic fitness journey.

### What it does
With Put Me In – the world's first personal coach on your arm, adaptable to multiple sports – you have professional guidance at your fingertips. Our smart sleeve, driven by cutting-edge machine learning, assesses your movements across sports like basketball and weightlifting, offering personalized insights for improvement. But it doesn't stop there – it also tracks your progress, ensuring safer and more effective workouts.

### Market sizing & demand
Every year, there are approximately $5 billion (TAM) spent on hiring an athletic trainer from amateur and other levels of non-professional athletes, and their average expense hourly is about $50-150. We've connected with 30 athletes on different levels, ranging from college varsity team members playing below NCAA D2 to amateur fitness athletes, and researched that their willingness to pay for training purposes is about maxi 200 USD per month. Taking into other necessary data accounts, we have a Serviceable Available Market (SAM) of about 1 billion per year.

### How we built it
We stitched together a sleeve that places 3 IMU sensors on the bicep, forearm, and hand. One of the greatest challenges in tracking sports performance with sensors is that labelled data can be costly to acquire, and so it is vital to find efficient algorithms to classify or analyze these types of movements and sensor data. We developed a dynamic time warping-based time series classification algorithm that is label-efficient, highly generalizable across sport modalities and different individuals, and lightweight enough to run on a Raspberry Pi that we have detachable from our wearable sleeve.

To get all these relevant data and insights to our users, we built a web app in Reflex. When you put on a sleeve and begin shooting, the data from the sensor gets transferred to our web app. There, we display a visualization of your practice movement (shot or weightlift). This visualization is rendered via a custom kinematics-based positional updating that we do to track relative positioning of the sensors based on accelerometer and gyro axes. Simultaneously, based on our machine learning motion analysis and DTW-based classification of your athletic form, we will display feedback on how your form could be improved. The web app also allows users to log into their accounts for an existing wearable such as a Garmin watch, and include that supplementary data. Finally, the web app also includes a viewer for video tutorials from Youtube trainers (which we envision could one day be a suite of “Put Me In” personal trainers and their video lessons.)

### What's next for Put Me In, Coach
Our vision for what's coming next? To democratize elite fitness technology for everyone. We want to use our model and expand it to a much greater variety of sports from arm-involved sports to lower-limbed focused programs such as football, etc. Through an affordable monthly subscription, equivalent to just a few hours with a traditional trainer, Put Me In brings professional coaching within reach. And with Put Me In, training becomes not only professional but enjoyable too. Don't wait – elevate your game with Put Me In today.

### Built With

Python, Reflex, Raspberry Pi, 3 IMUs (accelerometers)

#### Devpost link: https://devpost.com/software/put-me-in-coach
