import cv2
import numpy as np
from exceptions import *
import multiprocessing as mlt
import time

class kmeans_plus_plus:
    def __init__(self,k_value=3,image_path=None):
        self.k=k_value
        self.__image_path=image_path
        self.error=100
        self.max_int=1000000
        

    @property
    def k(self):
        return self.__k
    
    @k.setter
    def k(self,value):
        if(value<0 or value>100):
            raise kValueError()
        else:
            self.__k=value
    
    @property
    def image_path(self):
        return self.__image_path
    
    @image_path.setter
    def image_path(self,value):
        if(value==None or value==""):
            raise ImagePathError()
        else:
            self.__image_path=value
    
    def distance(self,point1,point2):
        sum_=0
        for ch in range(self.channels):
            sum_+=( ( int(point1[ch]) - int(point2[ch]) )**2 )
        return sum_ 


    

    # kmeans++ initialization takes place here
    
    def init_centroids(self,image):
        centroids=[image[np.random.randint(0,self.rows)][np.random.randint(0,self.cols)]]
        
        for center in range(self.k-1):
            candidate_distance=0
            candidate_rgb=[]
            for x in range(self.rows):
                for y in range(self.cols):
                    tmp_dist=self.max_int
                    rgb=[]
                    for c in centroids:
                        distance=self.distance(image[x][y],c)
                        if(distance<tmp_dist):
                            tmp_dist=distance
                            rgb=image[x][y]

                    if(candidate_distance<tmp_dist):
                        candidate_rgb=rgb
                        candidate_distance=tmp_dist
            centroids.append(candidate_rgb)
        
        self.__centroids=centroids
    
    def train(self,image):
        init_segments={}
        counts={}
        for center in self.__centroids:
            counts[tuple(center)]=0
            if(self.channels==3):
                init_segments[tuple(center)]=[0,0,0]
            elif(self.channels==1):
                init_segments[center]=0

        for x in range(self.rows):
            for y in range(self.cols):
                dist=self.max_int
                center_point=None
                for _,center in enumerate(self.__centroids):
                    temp_distance=self.distance(center,image[x][y])
                    if(temp_distance<dist):
                        dist=temp_distance
                        center_point=center
                init_segments[tuple(center_point)]=[x+y for x,y in zip(init_segments[tuple(center_point)],image[x][y])]
                counts[tuple(center_point)]+=1
        
        for center in self.__centroids:
            if(self.channels==1):
                init_segments[tuple(center)]=init_segments[tuple(center)][0]//counts[tuple(center)]
            else:
                for ch in range(self.channels):
                    init_segments[tuple(center)][ch]=init_segments[tuple(center)][ch]//counts[tuple(center)]


        old_centroids=self.__centroids.copy()
        self.__centroids=list(init_segments.values()).copy()
        error=0

        for count,center in enumerate( old_centroids ):
            error+=sum( [ abs(x-y) for x,y in zip(center,self.__centroids[count]) ] )
        
        self.error=error

    def __segment(self,image):

        for x in range(self.rows):
            for y in range(self.cols):
                dist=self.max_int
                center=None
                for centroid in self.__centroids:
                    temp=self.distance(image[x][y],centroid)
                    if(temp<dist):
                        center=centroid
                        dist=temp
                image[x][y]=center
        cv2.imshow("widnow",image)
        cv2.waitKey(0)


    def start(self):
        image=cv2.imread(self.image_path)
        self.rows,self.cols,self.channels=image.shape
        print("\nTraining started !")
        start=time.time()
        self.init_centroids(image)
        print("Centroid Initialization completed ! ")
        self.train(image)
        # chnage function do not passs image
        show_info= lambda error,centroids : print("Error : {} px , Centroids : {}".format(error,centroids))

        while(self.error>3):
            self.train(image)
            show_info(self.error,self.__centroids)
        print("Training completed !")
        print("Total time spent : {} sec".format(time.time()-start))
        self.__segment(image)

