## K means++ Image Segmentation
> **Note:** The **K means++** is improved version of **K means** it initializes centroids which helps to converge fast and avoid any clustering problems . Just first phase which is initialization is different in Kmeans++ however rest of the algorithms are same.

Instead randomly initialization it picks first one randomly and for the rest  best centroid matches selection performed .

Here are some results 
Real Image 
> ![tree](https://user-images.githubusercontent.com/39130214/72843548-2d4ca900-3cb4-11ea-80f7-4d72d6da7a5d.png)

k=3  best case : 18 seconds (on CPU 1 thread)  
> ![segmentk3](https://user-images.githubusercontent.com/39130214/72843328-ba433280-3cb3-11ea-9030-f3382987349c.png)

k=5 best case 30 sec (on CPU 1 thread)
>![segmentk5](https://user-images.githubusercontent.com/39130214/72843403-e199ff80-3cb3-11ea-98b9-6b456201887e.png)


> Requirements :

> OpenCV for python : cv2

> numerical computation library : numpy
