import cv2
import numpy as np
from .exceptions import *
import multiprocessing as mlt
import time

class kmeansPP:
    def __init__(self,k_value=3,image_path=None):
        self.k=k_value
        self.image_path=image_path
        self.error=100
        self.max_int=1000000
        

    def euclidieanDistance(self,point1,point2):
        sum_=0
        for ch in range(self.channels):
            sum_+=( ( int(point1[ch]) - int(point2[ch]) )**2 )
        return sum_ 


    # kmeans++ initialization takes place here
    # first centroid must be random point
    # rest are the points which maximizes distance to one another

    def initCentroids(self,image):
        centroids=[image[np.random.randint(0,self.rows)][np.random.randint(0,self.cols)]]
        
        for center in range(self.k-1):
            candidate_distance=0
            candidate_rgb=[]
            for x in range(self.rows):
                for y in range(self.cols):
                    tmp_dist=self.max_int
                    rgb=[]
                    for c in centroids:
                        distance=self.euclidieanDistance(image[x][y],c)
                        if(distance<tmp_dist):
                            tmp_dist=distance
                            rgb=image[x][y]

                    if(candidate_distance<tmp_dist):
                        candidate_rgb=rgb
                        candidate_distance=tmp_dist
            centroids.append(candidate_rgb)
        
        self.centroids=centroids
    
    # train kmeans here
    # standart kmeans algorithm except with good centroid initialization

    def train(self,image):
        init_segments={}
        counts={}
        error=0

        for center in self.centroids:
            counts[tuple(center)]=0
            if(self.channels==3):
                init_segments[tuple(center)]=[0,0,0]
            elif(self.channels==1):
                init_segments[center]=0

        for x in range(self.rows):
            for y in range(self.cols):
                dist=self.max_int
                center_point=None
                for _,center in enumerate(self.centroids):
                    temp_distance=self.euclidieanDistance(center,image[x][y])
                    if(temp_distance<dist):
                        dist=temp_distance
                        center_point=center
                init_segments[tuple(center_point)]=[x+y for x,y in zip(init_segments[tuple(center_point)],image[x][y])]
                counts[tuple(center_point)]+=1
        
        for center in self.centroids:
            if(self.channels==1):
                init_segments[tuple(center)]=init_segments[tuple(center)][0]//counts[tuple(center)]
            else:
                for ch in range(self.channels):
                    init_segments[tuple(center)][ch]=init_segments[tuple(center)][ch]//counts[tuple(center)]


        old_centroids=self.centroids.copy()
        self.centroids=list(init_segments.values()).copy()
        
        for count,center in enumerate( old_centroids ):
            error+=sum( [ abs(x-y) for x,y in zip(center,self.centroids[count]) ] )
        
        self.error=error

    # segmentation takes place here
    # check every point which locates nearby the centroid 
    # its value will be replaced with centroid 

    def segment(self,image):
        for x in range(self.rows):
            for y in range(self.cols):
                dist=self.max_int
                center=None
                for centroid in self.centroids:
                    temp=self.euclidieanDistance(image[x][y],centroid)
                    if(temp<dist):
                        center=centroid
                        dist=temp
                image[x][y]=center
        cv2.imshow("Segmentation",image)
        cv2.waitKey(0)


    def start(self):
        image=cv2.imread(self.image_path)
        self.rows,self.cols,self.channels=image.shape
        print("\nTraining started !")
        start=time.time()
        self.initCentroids(image)
        print("Centroid Initialization completed ! ")
        self.train(image)
        
        show_info= lambda error,centroids : print("Error : {} px , Centroids : {}".format(error,centroids))

        while(self.error>3):
            self.train(image)
            show_info(self.error,self.centroids)
        print("Training completed !")
        print("Total time spent : {} sec".format(time.time()-start))
        self.segment(image)

