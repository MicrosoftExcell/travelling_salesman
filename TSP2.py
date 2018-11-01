#genetic algorithm
#reading file
for k in range(50):
    import random
    f = open("NEWAISearchfile012.txt","r")
    contents = f.read()
    f.close()
    tour_size = 0
    dists = []
    edges = []
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
    def find_length(tour):
        global tour_size
        tour_size = 0
        for i in range(len(tour)-1):
            tour_size+=edges[tour[i]][tour[i+1]]
        tour_size+=edges[tour[-1]][tour[0]]
        return(tour_size)

    #mutates tour - swaps 2 cities
    def mutation(tour):
        copy = []
        for i in range(len(tour)):
            copy.append(tour[i])
        city1 = random.randint(0,size-2)
        city2 = random.randint(city1+1,size-1)
        tour[city1] = copy[city2]
        tour[city2] = copy[city1]
        return tour

    #generates crossover
    def crossover(tour1,tour2):
        global size
        city1 = random.randint(0,size-3)
        city2 = random.randint(city1+1,size-1)
        child = []
        missing = []
        included = []
        repeated = []
        locations = []
        #section of tour2 put into tour 1
        for i in range(city1):
            child.append(tour1[i])
        for i in range(city1,city2+1):
            child.append(tour2[i])
        for i in range(city2+1,size):
            child.append(tour1[i])
        #swapping the the first of each repetition with a missing number            
        for i in range(size):
            if child[i] not in included:
                included.append(child[i])
            else:
                repeated.append(child[i])
        for i in range(size):
            if child[i] in repeated:
                locations.append(i)
                for j in range(len(repeated)):
                    if repeated[j] == child[i]:
                        del repeated[j]
                        break
        for i in range(size):
            if i not in included:
                missing.append(i)
        for i in range(len(locations)):
            child[locations[i]] = missing[i]
        return child

    def crossover2(tour1,tour2):
        global size
        city1 = random.randint(0,size-3)
        city2 = random.randint(city1+1,size-1)
        child1 = []
        child2 = []
        middle1 = []
        middle2 = []
        children = []
        for i in range(city1,city2+1):
            middle1.append(tour1[i])
        for i in range(city1,city2+1):
            middle2.append(tour2[i])
        pointer = 0
        k = 0
        while pointer!=city1:
            if tour2[k] not in middle1:
                child1.append(tour2[k])
                pointer+=1
            k+=1
        for i in range(len(middle1)):
            child1.append(middle1[i])
        while len(child1)<size:
            for i in range(k,size):
                if tour2[i] not in child1:
                    child1.append(tour2[i])
        pointer = 0
        k = 0
        while pointer!=city1:
            if tour1[k] not in middle2:
                child2.append(tour1[k])
                pointer+=1
            k+=1
        for i in range(len(middle2)):
            child2.append(middle2[i])
        while len(child2)<size:
            for i in range(k,size):
                if tour1[i] not in child2:
                    child2.append(tour1[i])
        children.append(child1)
        children.append(child2)
        return children

        
    #generates random tour through cities
    def generate_tour():
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
        return tour

    tours = []
    lengths = []
    parents = []
    pop_size = 100 # must increase with number of cities
    crossover_prob = 0.55 # so some good parents will carry on/others will create variety
    mutation_prob = 0.1 # more cities already have more variation so need smaller mutation prob
    for i in range(pop_size):
        new_tour = generate_tour()
        tours.append(new_tour)
        length = find_length(new_tour)
        lengths.append(length)
    for i in range(10000): # fewer generations need as pop size increases
        #mutation_prob+=0.0000001 # more mutations as tours become more and more similar
        length_sum = 0
        for i in range(len(lengths)):
            length_sum+=lengths[i]
        probs = []
        for i in range(len(lengths)):
            prob = lengths[i]/length_sum
            prob = 1/prob # so smaller tours have higher fitness
            probs.append(prob)
        probs_sum = 0
        for i in range(len(probs)):
            probs_sum+=probs[i]
        for j in range(pop_size):
            num = random.uniform(0,probs_sum)
            total = 0
            for i in range(len(probs)):
                if num<total+probs[i] and num>=total:
                    parents.append(tours[i])
                    break
                else:
                    total+=probs[i]
        offspring = []
        for i in range(int(pop_size/2)):
            num1 = random.randint(0,len(parents)-1)
            parent1 = parents[num1]
            del parents[num1]
            num2 = random.randint(0,len(parents)-1)
            parent2 = parents[num2]
            del parents[num2]
            cross = random.uniform(0,1)
            mutant = random.uniform(0,1)
            if cross<crossover_prob:
                child1 = crossover(parent1,parent2)
                child2 = crossover(parent2,parent1)
                #children = []
                #children = crossover2(parent1,parent2)
                #child1 = children[0]
                #child2 = children[1]
                if mutant<mutation_prob:
                    child1 = mutation(child1)
                    child2 = mutation(child2)
                offspring.append(child1)
                offspring.append(child2)
            else:
                if mutant<mutation_prob:
                    parent1 = mutation(parent1)
                    parent2 = mutation(parent2)
                offspring.append(parent1)
                offspring.append(parent2)
        lengths = []
        for i in range(len(offspring)):
            length = find_length(offspring[i])
            lengths.append(length)
        tours = []
        for i in range(len(offspring)):
            tours.append(offspring[i])
    print(lengths,"\n")
    small = min(lengths)
    print(small)
    best_tour = []
    for i in range(len(lengths)):
        if lengths[i] == small:
            best_tour = tours[i]
    for i in range(len(best_tour)):
        best_tour[i]+=1
    print(best_tour)
    
