import numpy as np
import random
import math

class GA:
    def __init__(self, Generation,  ClassRoom, Subject, MeetingTime, Teacher, Date, Max_course_per_day, mutation,
                 numberOfPopulation):
        self.Generation = Generation
        self.ClassRoom = ClassRoom
        self.Subject = Subject
        self.MeetingTime = MeetingTime
        self.Teacher = Teacher
        self.Date = Date
        self.Max_course_per_day = Max_course_per_day
        self.mutation = mutation
        self.numberOfPopulation = numberOfPopulation
        self.population_score = []

    def InitPopulation(self):
        generate = []
        for _ in range(100):
            schedule = []
            for i in self.Subject:
                for j in range((self.Subject[i])):
                    a = [i, random.choice(self.ClassRoom), random.choice(self.MeetingTime),
                         random.choice(
                             [teacher for teacher in self.Teacher if i in self.Teacher[teacher]]),
                         random.choice(self.Date)]
                    schedule.append(a)
            generate.append(schedule)
        return generate

    def calcFitness(self, individual):
        score = 0
        count_class_per_day = 0
        #moi nguoi deu co ca day trong 1 tuan(ưu tiên)
        name_teacher = list(set(map(lambda x: x, self.Teacher)))
        teacher_name_schedule = list(set(map(lambda x: x[3], individual)))
        if len(name_teacher) == len(teacher_name_schedule):
            score -= 0.01

        for i in range(len(individual)):
            if (individual[i][0] not in self.Teacher[individual[i][3]]):
                score += 3
            individual_sort_name = sorted(individual, key=lambda x: x[3])
            for j in range(len(individual)):
                # 2 mon 1 phong tai 1 thoi diem
                if (i != j) and (individual[j][1] == individual[i][1]) and (individual[j][2] == individual[i][2]) and (
                        individual[j][-1] == individual[i][-1]):
                    score += 1
                # 1 nguoi day 2 phong tai 1 thoi diem
                if (i != j) and (individual[j][3] == individual[i][3]) and (individual[j][2] == individual[i][2]) and (
                        individual[j][-1] == individual[i][-1]):
                    score += 1
                # uu tien day 2 ca trong 1 toa nha:
                if (i != j) and (individual[j][-1] == individual[i][-1]) and (
                        individual[j][3] == individual[i][3]) and (
                        individual[j][1][0] == individual[i][1][0]):
                    score -= 0.01
                # 1 nguoi toi da day trong 1 ngay
                if i != j and individual_sort_name[j][3] == individual_sort_name[i][3] and individual_sort_name[j][
                    -1] == \
                        individual_sort_name[i][-1]:
                    count_class_per_day += 0.5
                else:
                    count_class_per_day = 0
                if count_class_per_day + 1 == self.Max_course_per_day:
                    score += 0.5

        return score

    def chonloc(self):
        # sort with score thap den cao
        new_population_score = []
        for i in self.population_score:
            if i not in new_population_score:
                new_population_score.append(i)

        self.population_score = new_population_score
        self.population_score = sorted(
            self.population_score, key=lambda x: x[-1])
        self.population_score = self.population_score[:self.numberOfPopulation]
        # return self.population_score[:math.floor(0.8 * len(self.population_score))]

    def laighep(self):
        for i in range((len(self.population_score) - 1)):
            con = []
            # cha = self.population_score[i][0]
            # me = self.population_score[i + 1][0]
            cha = random.choice(self.population_score)[0]
            me = random.choice(self.population_score)[0]
            center = len(cha) // 2
            con.append(cha[0:center] + me[center:len(me)])
            con.append(self.calcFitness(con[0]))
            self.population_score.append(con.copy())

    def dotbien(self):
        for _ in range(int(len(self.population_score) * self.mutation)):
            selection = random.choice(self.population_score).copy()
            i = random.randint(0, len(selection[0])-1)
            time = random.choice(self.MeetingTime)
            date = random.choice(self.Date)
            class_room = random.choice(self.ClassRoom)
            new_gen = random.choice(self.population_score)[0][i].copy()
            new_gen[1] = class_room
            new_gen[2] = time
            new_gen[4] = date
            new_child = []
            
            new_child.append(selection[0].copy())
            new_child[0][i] = new_gen
            new_child.append(self.calcFitness(new_child[0]))
            self.population_score.append(new_child)

    def schedule(self):
        #valid input
        temp = list(map(lambda x: self.Teacher[x], self.Teacher))
        checksub = []
        for i in temp:
            checksub += [j for j in i]
        delitem = []
        for i in self.Subject:
            if(i not in checksub):
                delitem.append(i)
        for i in delitem:
            del self.Subject[i]

        for i in self.Teacher:
            delsub = []
            for j in self.Teacher[i]:
                if j not in self.Subject:
                    delsub.append(j)
            for j in delsub:
                self.Teacher[i].remove(j)

        population = self.InitPopulation()
        self.population_score = list(
            map(lambda x: [x, self.calcFitness(x)], population))
        self.population_score = sorted(
            self.population_score, key=lambda x: x[-1])

        for _ in range(self.Generation):

            self.laighep()

            self.dotbien()
            self.chonloc()

            if self.population_score[0][1] <= 0:
                break
        return self.population_score[0]
