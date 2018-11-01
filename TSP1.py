#simulated annealing
#reading file
for k in range(200):
    import random
    #filename = input("Enter name of file (e.g. AISearchtestcase.txt): ")
    f = open("NEWAISearchfile535.txt","r")
    contents = f.read()
    f.close()
    tour_size = 0
    dists = []
    edges = []
    temperature = 10000
    numbers = ["0","1","2","3","4","5","6","7","8","9"]
    for i in contents.split(","):
        dists.append(i.strip())
    dists[1] = dists[1].replace("SIZE = ","")
    name = dists[0]
    del dists[0]
    size = int(dists[0])
    del dists[0]
    for i in range(len(dists)):
        if dists[i].isdigit() == False:
            for j in range(len(dists[i])):
                if dists[i][j] not in numbers:
                    dists[i] = dists[i].replace(dists[i][j],"")
    point = -1
    for i in range(size):
        edges.append([])
        for j in range(size):
            if j==i:
                edges[i].append(0)
            elif i==0:
                point+=1
                edges[i].append(int(dists[point]))
            elif j<i:
                edges[i].append(edges[j][i])
            else:
                point+=1
                edges[i].append(int(dists[point]))

    #function to find size of tour
    def find_length():
        global tour_size
        tour_size = 0
        for i in range(len(tour)-1):
            tour_size+=edges[tour[i]][tour[i+1]]
        tour_size+=edges[tour[-1]][tour[0]]
        return(tour_size)
            
    #start with random tour through cities
    tour = []
    length = []
    temp = 0
    for i in range(size):
        length.append(temp)
        temp+=1
    for i in range(size):
        num = random.randint(0,len(length)-1)
        tour.append(length[num])
        del length[num]
    tour1 = find_length()

    #using the temperature to determine when to stop
    iterations = 0
    while temperature > 1:
        iterations+=1
        count = 0
        while count<=100:
            #reverse a small subset of cities in tour and find length
            count+=1
            copy = []
            for i in range(len(tour)):
                copy.append(tour[i])
            city1 = random.randint(0,size-3)
            city2 = random.randint(city1+1,size-1)
            diff = city2-city1
            for i in range(0,diff+1):
                tour[city2-i] = copy[city1+i]
            tour2 = find_length()
            #comparing the lengths to choose which tour to continue with
            diff = tour2-tour1
            prob = 2.71828**(-diff/temperature)
            r = random.uniform(0.0,1.0)
            if tour2<=tour1:
                tour1 = tour2
            elif r < prob:
                tour1 = tour2
            else:
                tour = []
                for i in range(len(copy)):
                     tour.append(copy[i])
        #decrease temperature after every iteration
        temperature = 10000/(1+0.9*iterations)
    end_size = find_length()
    print(end_size)
    for i in range(size):
        tour[i]+=1
    print(tour)
    
