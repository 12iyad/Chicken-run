import pygame, time, random, os, math, sqlite3, hashlib
import tkinter as tk
import LevelAI as la


def loginsystem():
    global db
    global c
    db = sqlite3.connect('database.db')
    c = db.cursor()
    #SQL function called after registered values inputted by user
    def SQLReg(user, passw):
        c.execute("INSERT INTO accounts(username, password, level) VALUES('{}', '{}', '0')".format(user, passw))
        db.commit()
    #Register gui using tkinter
    def reggui(parent):
        if parent == "logORreg":
            root.destroy()
        if parent == "login":
            rootLogin.destroy()
        global rootReg
        rootReg = tk.Tk()
        window1 = tk.Canvas(rootReg, width = 400, height=300)
        window1.pack()

        username = tk.Entry(rootReg)
        password = tk.Entry(rootReg, show="*")
        username.configure({"highlightbackground":"red"})
        #replace password characters with *
        password_confirm = tk.Entry(rootReg, show="*")
        usernameText = tk.Label(rootReg, text = 'Username:')
        passwordText = tk.Label(rootReg, text = 'Password:')
        password_confirmText = tk.Label(rootReg, text = 'Confirm password:')
        window1.create_window(100, 110, window=usernameText)
        window1.create_window(100, 140, window=passwordText)
        window1.create_window(77, 170, window=password_confirmText)
        window1.create_window(200, 140, window=password)
        window1.create_window(200, 110, window=username)
        window1.create_window(200, 170, window=password_confirm)
        emptyEntry = tk.Label(rootReg, text = 'Values must be over 2 characters!')
        unmatchedPass = tk.Label(rootReg, text = 'Passwords do\n not match!')
        userExists = tk.Label(rootReg, text = 'Username already exists try another!')
        emptyEntry.configure({"background":"red"})
        unmatchedPass.configure({"background":"red"})
        
        #Check username does not already exist
        def register():
            usernameInput = username.get()
            if len(usernameInput) <= 2:
                window1.create_window(200, 50, window=emptyEntry)
                
            else:
                c.execute("SELECT username FROM accounts WHERE username = (?)", (usernameInput,))
                userresult = c.fetchall()
                if len(userresult) > 0:
                    window1.create_window(200, 50, window=userExists)
                else:
                    if password.get() == password_confirm.get():
                        if len(password.get()) <= 2:
                            window1.create_window(200, 50, window=emptyEntry)

                        else:
                            passwordInput = password.get()
                            SQLReg(usernameInput, passwordInput)
                            logingui("register")
                    
                    else:
                        window1.create_window(310, 155, window=unmatchedPass)
                  
        registerButton = tk.Button(text='Register', command=register)
        window1.create_window(200, 200, window = registerButton)
        loginButton = tk.Button(rootReg, text='Login', command= lambda: logingui("register"))
        window1.create_window(40, 280, window = loginButton)
        
    def logingui(parent):
        if parent == "logORreg":
            root.destroy()
        if parent == "register":
            rootReg.destroy()
        global rootLogin
        rootLogin = tk.Tk()
        window1 = tk.Canvas(rootLogin, width = 400, height = 300)
        window1.pack()

        username = tk.Entry(rootLogin)
        password = tk.Entry(rootLogin, show="*")
        usernameText = tk.Label(rootLogin, text = 'Username:')
        passwordText = tk.Label(rootLogin, text = 'Password:')
        incorrectUorP = tk.Label(rootLogin, text = 'Incorrect username or password!')
        window1.create_window(100, 110, window=usernameText)
        window1.create_window(100, 140, window=passwordText)
        window1.create_window(200, 140, window=password)
        window1.create_window(200, 110, window=username)
        incorrectUorP.configure(background="red")
        

        def login():
            usernameInput = username.get()
            c.execute("SELECT username FROM accounts WHERE username = (?)", (usernameInput,))
            global userresult
            userresult = c.fetchone()
            #Check for incorrect password
            if len(userresult) == 0:
                window1.create_window(200, 50, window=incorrectUorP)

            
            else:
                passwordInput = password.get()

                c.execute("SELECT password FROM accounts WHERE username = (?) AND password = (?)", (usernameInput, passwordInput))
                passresult = c.fetchall()
                if len(passresult) == 0:
                    window1.create_window(200, 50, window=incorrectUorP)
                else:
                    print("Successfully logged in")
                    
                    rootLogin.destroy()
                    usernameCheck = userresult
                    menu(usernameCheck)
                    

        loginButton = tk.Button(text='Login', command=login)
        window1.create_window(200, 170, window = loginButton)
        registerButton = tk.Button(rootLogin, text='Register', command= lambda: reggui("login"))
        window1.create_window(40, 280, window = registerButton)

        
        
    
        
    def logORreg():
        global root
        root = tk.Tk()
        window1 = tk.Canvas(root, width = 400, height = 300)
        window1.pack()
        
        loginButton = tk.Button(text='Login', command= lambda: logingui("logORreg"))
        window1.create_window(200, 140, window = loginButton)
        regButton = tk.Button(text='Register', command= lambda: reggui("logORreg"))
        window1.create_window(200, 180, window = regButton)
        
    logORreg()
    
def play(usernameCheck):
    pygame.init()
    win = pygame.display.set_mode((640, 607))
    pygame.display.set_caption("Chicken Run")
    favicon = pygame.image.load('up1.png')
    pygame.display.set_icon(favicon)
    winx = 640
    winy = 602
    point = 0
    walkRight = [pygame.image.load('right1.png'), pygame.image.load('right2.png'), pygame.image.load('right3.png'), pygame.image.load('right1.png'), pygame.image.load('right2.png'), pygame.image.load('right3.png'), pygame.image.load('right1.png'), pygame.image.load('right2.png'), pygame.image.load('right3.png'), ]
    walkLeft = [pygame.image.load('left1.png'), pygame.image.load('left2.png'), pygame.image.load('left2.png'), pygame.image.load('left1.png'), pygame.image.load('left2.png'), pygame.image.load('left2.png'), pygame.image.load('left1.png'), pygame.image.load('left2.png'), pygame.image.load('left2.png'), ]
    walkUp = [pygame.image.load('up1.png'), pygame.image.load('up2.png'), pygame.image.load('up3.png'), pygame.image.load('up1.png'), pygame.image.load('up2.png'), pygame.image.load('up3.png'), pygame.image.load('up1.png'), pygame.image.load('up2.png'), pygame.image.load('up3.png'), pygame.image.load('up1.png'), pygame.image.load('up2.png'), pygame.image.load('up3.png'), pygame.image.load('up1.png'), pygame.image.load('up2.png'), pygame.image.load('up3.png'), pygame.image.load('up1.png'), pygame.image.load('up2.png'), pygame.image.load('up3.png'), ]
    walkDown = [pygame.image.load('down1.png'), pygame.image.load('down2.png'), pygame.image.load('down3.png'), pygame.image.load('down1.png'), pygame.image.load('down2.png'), pygame.image.load('down3.png'), pygame.image.load('down1.png'), pygame.image.load('down2.png'), pygame.image.load('down3.png'), pygame.image.load('down1.png'), pygame.image.load('down2.png'), pygame.image.load('down3.png'), pygame.image.load('down1.png'), pygame.image.load('down2.png'), pygame.image.load('down3.png'), pygame.image.load('down1.png'), pygame.image.load('down2.png'), pygame.image.load('down3.png'), ]
    bg = pygame.image.load('background.png')
    overlay = pygame.image.load('treeoverlay.png')
    chickenIMG = pygame.image.load('up2.png')
    eggIMG = pygame.image.load('egg.png')
    nestIMG = pygame.image.load('nest.png')
    play = pygame.image.load('play.png')
    lifeIMG = pygame.transform.scale(pygame.image.load('left2.png'), (22, 22))
    pygame.transform.scale(pygame.image.load('play.png'),(300,100))

    white = (255, 255, 255) 
    green = (0, 255, 0) 
    blue = (0, 0, 128) 
    X = 600
    Y = 590

    


    clock = pygame.time.Clock()

    class player():
        def __init__(self, x, y, width, height, level):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.level = int(level)
            self.vel = 3
            self.left = False
            self.right = False
            self.up = False
            self.down = False
            self.life1 = True
            self.life2 = True
            self.life3 = True
            self.frame = 0
            self.hitbox = (self.x, self.y, self.width, self.height)
            self.lives = 3


        def draw(self,win):
            if self.frame + 1 >= 27:
                self.frame = 0
                
            if self.left:
                win.blit(walkLeft[self.frame//3], (self.x,self.y))
                self.frame += 1
                
            elif self.right:
                win.blit(walkRight[self.frame//3], (self.x,self.y))
                self.frame +=1
                
            elif self.up:
                win.blit(walkUp[self.frame//3], (self.x,self.y))
                self.frame +=1
                
            elif self.down:
                win.blit(walkDown[self.frame//3], (self.x,self.y))
                self.frame +=1
                
            else:
                win.blit(chickenIMG, (self.x,self.y))

            if self.life3:
                win.blit(lifeIMG, (30, 20))

            if self.life2:
                win.blit(lifeIMG, (54, 20))

            if self.life1:
                win.blit(lifeIMG, (78, 20))                
                
                    
            self.hitbox = (self.x, self.y+4, self.width, 40)
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)
            

        def collision(self):
            time.sleep(1)
            self.QuestionsAI()
            self.lives -= 1
            self.x = 550
            self.y = 550
            
            if self.lives == 2:
                self.life1 = False

                
            elif self.lives == 1:
                self.life2 = False

                
            elif self.lives == 0:
                self.life3 = False

                
                fadegame()
                endgamescreen(usernameCheck)
                menu(usernameCheck)

        def QuestionsAI(self):
            backgroundButton = pygame.transform.scale(pygame.image.load('backgroundButton.png'),(300,100))
            backgroundButtonTest = pygame.transform.scale(pygame.image.load('play.png'),(300,100))
            list1 = [120, 240, 350]

            pygame.display.update()
            class questionsPicker():
                def __init__(self, level):
                    numList1 = [random.randint(0, 6),
                               random.randint(0, 12),
                               random.randint(0, 30),
                               random.randint(0, 40),
                               random.randint(0, 50),
                               random.randint(0, 60),
                               random.randint(0, 70),
                               random.randint(0, 80),
                               random.randint(0, 90),
                               random.randint(0, 100)]
                    
                    numList2 = [random.randint(0, 6),
                               random.randint(0, 12),
                               random.randint(0, 30),
                               random.randint(0, 40),
                               random.randint(0, 50),
                               random.randint(0, 60),
                               random.randint(0, 70),
                               random.randint(0, 80),
                               random.randint(0, 90),
                               random.randint(0, 100)]
                    
                    
                    
                    if int(level) >= 10:
                        self.level = 9

                    elif int(level) <= 0:
                        self.level = 0
                        
                    else:
                        self.level = level
                        
                    self.wrong1 = True
                    self.wrong2 = True
                    self.correct = True

                    self.CorrectX = random.randint(0,330)
                    self.Wrong1X = random.randint(0,330)
                    self.Wrong2X = random.randint(0,330)
                    
                    self.CorrectY = random.choice(list1)
                    list1.remove(self.CorrectY)
                    
                    self.Wrong1Y = random.choice(list1)
                    list1.remove(self.Wrong1Y)
                    
                    self.Wrong2Y = random.choice(list1)
                    self.ListY = [120, 240, 350]

                    self.num1 = numList1[int(self.level)]
                    self.num2 = numList2[int(self.level)]
                                        
                    self.correctHitbox = pygame.Rect((self.CorrectX,self.CorrectY), (300,100))
                    self.Wrong1Hitbox = pygame.Rect((self.Wrong1X,self.Wrong1Y), (300,100))
                    self.Wrong2Hitbox = pygame.Rect((self.Wrong2X,self.Wrong2Y), (300,100))

                    #Depending on level operation will change difficulty
                    print(self.level)
                    if self.level <= 2:
                        self.operation = '+'

                    if self.level <= 3:
                        self.operation = random.choice(['+', '-'])

                    if self.level <=5:
                        self.operation = random.choice(['+', '-', 'x'])

                    if self.level >= 8:
                        self.operation = random.choice(['+', '-', 'x' , '/'])
                    
                def Collision(self):
                    self.CorrectX = random.randint(0,330)
                    self.Wrong1X = random.randint(0,330)
                    self.Wrong2X = random.randint(0,330)
                    self.CorrectY = random.choice(list1)
                    list1.remove(self.CorrectY)
                    self.Wrong1Y = random.choice(list1)
                    list1.remove(self.Wrong1Y)
                    self.Wrong2Y = random.choice(list1)
                    self.List1 = [120, 240, 350]
                    
                    self.correctHitbox = pygame.Rect((self.CorrectX,self.CorrectY), (300,100))
                    self.Wrong1Hitbox = pygame.Rect((self.Wrong1X,self.Wrong1Y), (300,100))
                    self.Wrong2Hitbox = pygame.Rect((self.Wrong2X,self.Wrong2Y), (300,100))
                    return

                def textGen(self):
                    X  = CorrectX + 150 
                    self.font = pygame.font.Font('freesansbold.ttf', 16)
                    self.text = self.font.render("Test", True, (0,0,0),)
                    self.textRect = self.text.get_rect()
                    self.textRect.center = (X, Y)
                    win.blit(self.text, self.textRect)




            def spriteGen():
                win.blit(bg, (0,0))
                correctX  = questions.CorrectX + 150
                correctY = questions.CorrectY + 47
                wrong1X  = questions.Wrong1X + 150
                wrong1Y = questions.Wrong1Y + 47
                wrong2X  = questions.Wrong2X + 150
                wrong2Y = questions.Wrong2Y + 47
                #Dictionary data whichever operation chosen will give out the chosen function
                opSolver = {'+': lambda a,b : a+b,
                            '-': lambda a, b: a-b,
                            'x': lambda a, b: a*b,
                            '/': lambda a, b: a/b}
                
                opSolverWrong1 = {'+': lambda a,b : a+b+1,
                            '-': lambda a, b: a-b+1,
                            'x': lambda a, b: (a*b)+2,
                            '/': lambda a, b: b/a+a}
                
                opSolverWrong2 = {'+': lambda a,b : a+b-1,
                            '-': lambda a, b: a-b-1,
                            'x': lambda a, b: (a*b)+1,
                            '/': lambda a, b: b/a}
                
                try:
                    print(questions.operation)
                    correctAns = opSolver[questions.operation](questions.num1, questions.num2)
                    wrong1Ans = opSolverWrong1[questions.operation](questions.num1, questions.num2)
                    wrong2Ans = opSolverWrong2[questions.operation](questions.num1, questions.num2)
                #if a/0 then denominator will change and called again
                except ZeroDivisionError:
                    questions.num2 += 1
                    correctAns = opSolver[questions.operation](questions.num1, questions.num2)
                    wrong1Ans = opSolverWrong1[questions.operation](questions.num1, questions.num2)
                    wrong2Ans = opSolverWrong2[questions.operation](questions.num1, questions.num2)
                    
                #Generate text depending on random number generated
                font = pygame.font.Font('freesansbold.ttf', 30)
                CorrectText = font.render(str(round(correctAns, 3)), True, (255,255,255),)
                Wrong1Text = font.render(str(round(wrong1Ans)), True, (255,255,255),)
                Wrong2Text = font.render(str(round(wrong2Ans)), True, (255,255,255),)
                CorrectTextRect = CorrectText.get_rect()
                Wrong1TextRect = Wrong1Text.get_rect()
                Wrong2TextRect = Wrong2Text.get_rect()
                CorrectTextRect.center = (correctX, correctY)
                Wrong1TextRect.center = (wrong1X, wrong1Y)
                Wrong2TextRect.center = (wrong2X, wrong2Y)
                #Load buttons with one correct button and 2 wrong buttons
                if questions.correct:
                    win.blit(backgroundButton, (questions.CorrectX,questions.CorrectY))
                    win.blit(CorrectText, CorrectTextRect)
                if questions.wrong1:
                    win.blit(backgroundButton, (questions.Wrong1X,questions.Wrong1Y))
                    win.blit(Wrong1Text, Wrong1TextRect)
                if questions.wrong2:
                    win.blit(backgroundButton, (questions.Wrong2X,questions.Wrong2Y))
                    win.blit(Wrong2Text, Wrong2TextRect)
                
                whatIStext = "What is " + str(questions.num1)+ " " + str(questions.operation) + " " + str(questions.num2)
                whatIS = font.render(whatIStext, True, (0,0,0),)
                win.blit(whatIS, (70, 50))
                
                pygame.display.update()   
            #c.execute("SELECT level FROM accounts WHERE username = (?)", (usernameCheckSTR,))
            #levelDB = c.fetchone()
            questions = questionsPicker(self.level)
            
            firstTry = True
            run = True
            
            while run:
                spriteGen()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1 and questions.correctHitbox.collidepoint(event.pos):
                        questions.correct = True
                        questions.wrong1 = False
                        questions.wrong2 = False
                        questions.Collision
                        print(firstTry)
                        if firstTry:
                            self.level += 0.25
                            print(self.level)
                            c.execute('UPDATE accounts SET level = (?) WHERE username = (?)', (self.level, usernameCheckSTR))
                            db.commit()
                        run = False
                        
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1 and questions.Wrong1Hitbox.collidepoint(event.pos):
                        self.level -= 0.10
                        print(self.level)
                        c.execute('UPDATE accounts SET level = (?) WHERE username = (?)', (self.level, usernameCheckSTR))
                        db.commit()
                        firstTry = False
                        print(firstTry)
                        questions.wrong1 = False

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1 and questions.Wrong2Hitbox.collidepoint(event.pos):
                        self.level -= 0.10
                        print(self.level)
                        c.execute('UPDATE accounts SET level = (?) WHERE username = (?)', (self.level, usernameCheckSTR))
                        db.commit()
                        firstTry = False
                        print(firstTry)
                        questions.wrong2 = False


            print(self.level)            
            return
            
                 

    class items():
        def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.hitbox = (self.x, self.y, self.width, self.height)

        def draw(self, win):
            win.blit(self.frame, (self.x,self.y))
            self.hitbox = (self.x, self.y, self.width, self.height)

    
    class egg(items):
        frame = eggIMG


    class nest(items):
        frame = nestIMG

    class car():
        
        def __init__(self, lc, x, width, height, end):
            self.lc = lc
            self.ticker = int(random.choice([-1, 1]))
            self.x = x
            self.y = int(random.choice(random.choice(self.lc)))
            self.width = width
            self.end = end
            self.height = height
            self.path = [self.x, self.end]
            self.frame = 0
            if self.ticker == -1:
                self.x = self.path[1]
                self.vel = random.randint(-20, -10)
            else:
                self.vel = random.randint(10, 20)
            self.switcherL = -1
            self.switcherR = 1
            self.hitbox = (self.x, self.y, self.width, self.height)
            
        def draw(self, win):
            if self.ticker == 1:
                self.moveRL()
            elif self.ticker == -1:
                self.moveLR()
            
            if self.frame + 1 >= 9:
                self.frame = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.frame //3], (self.x, self.y))
                self.frame += 1

            elif self.vel < 0:
                win.blit(self.walkLeft[self.frame //3], (self.x, self.y))
                self.frame += 1
            
            self.hitbox = (self.x, self.y, self.width, self.height)
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)
            
        def moveRL(self):
            if self.vel > 0:
                
                if self.x - self.vel < self.path[1]:
                    if self.switcherR == 1:
                        self.y = int(random.choice(self.lc[0]))
                        self.switcherR += 1
                    self.x += self.vel
                    
                else:
                    self.vel = self.vel * -1
                    self.frame = 0
                    self.switcherR = 1
                    
            elif self.vel < 0:

                if self.x + self.vel > self.path[0]:
                    if self.switcherL == -1:
                        self.y = int(random.choice(self.lc[1]))
                        self.switcherL -= 1
                    self.x += self.vel
                    
                else:
                    self.vel = self.vel * -1
                    self.frame = 0
                    self.switcherL = -1
                    
        def moveLR(self):
            if self.vel > 0:
                
                if self.x - self.vel < self.path[1]:
                    if self.switcherR == 1:
                        self.y = int(random.choice(self.lc[0]))
                        self.switcherR += 1
                    self.x += self.vel
                    
                else:
                    self.vel = self.vel * -1
                    self.frame = 0
                    self.switcherR = 1
                    
            elif self.vel < 0:

                if self.x + self.vel > self.path[0]:
                    if self.switcherL == -1:
                        self.y = int(random.choice(self.lc[1]))
                        self.switcherL -= 1
                    self.x += self.vel
                    
                else:
                    self.vel = self.vel * -1
                    self.frame = 0
                    self.switcherL = -1

    class textgen():
        def __init__(self, point):
            self.point = point
            self.datalog = -1
            self.i = -49
            
        def draw(self,win):
            if self.point == 1:
                pointplural = " Point"
            else:
                pointplural = " Points"
            self.pointStr = str(self.point) + pointplural
            self.font = pygame.font.Font('freesansbold.ttf', 16)
            self.text = self.font.render(self.pointStr, True, (255,0,0),)
            self.textRect = self.text.get_rect()
            self.textRect.center = (X, Y)
            win.blit(self.text, self.textRect)
            
                
            if self.i < 49:
                graph = int(-(1/10)*(int(self.i))**2 + 255)
                font = pygame.font.Font('freesansbold.ttf', int(graph/10))
##                c.execute("SELECT score FROM accounts WHERE username = (?)", (usernameCheck))
##                scoreresult = c.fetchone()
##                scoreresult = int(scoreresult[0]) + 1              
                text = font.render("Bring the egg back to the nest!", True, (255,255,255))
                surf = pygame.Surface(text.get_size()).convert_alpha()
            
                surf.fill((0, 0, 0, (graph)))
                text.blit(surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                win.blit(text, (110,25))
                self.i += 1
                
    
            
        
        

    class redCar(car):
        walkRight = [pygame.image.load('redcarright1.png'), pygame.image.load('redcarright2.png'), pygame.image.load('redcarright1.png'), pygame.image.load('redcarright2.png'),pygame.image.load('redcarright1.png'), pygame.image.load('redcarright2.png'),pygame.image.load('redcarright1.png'), pygame.image.load('redcarright2.png')]
        walkLeft = [pygame.image.load('redcarleft1.png'), pygame.image.load('redcarleft2.png'), pygame.image.load('redcarleft1.png'), pygame.image.load('redcarleft2.png'), pygame.image.load('redcarleft1.png'), pygame.image.load('redcarleft2.png'), pygame.image.load('redcarleft1.png'), pygame.image.load('redcarleft2.png')]

    class whiteBus(car):
        walkRight = [pygame.image.load('whitebusright1.png'), pygame.image.load('whitebusright2.png'), pygame.image.load('whitebusright1.png'), pygame.image.load('whitebusright2.png'), pygame.image.load('whitebusright1.png'), pygame.image.load('whitebusright2.png'), pygame.image.load('whitebusright1.png'), pygame.image.load('whitebusright2.png'), pygame.image.load('whitebusright1.png'), pygame.image.load('whitebusright2.png'), pygame.image.load('whitebusright1.png'), pygame.image.load('whitebusright2.png')]
        walkLeft = [pygame.image.load('whitebusleft1.png'), pygame.image.load('whitebusleft2.png'), pygame.image.load('whitebusleft1.png'), pygame.image.load('whitebusleft2.png'), pygame.image.load('whitebusleft1.png'), pygame.image.load('whitebusleft2.png'), pygame.image.load('whitebusleft1.png'), pygame.image.load('whitebusleft2.png'), pygame.image.load('whitebusleft1.png'), pygame.image.load('whitebusleft2.png'), pygame.image.load('whitebusleft1.png'), pygame.image.load('whitebusleft2.png')]

    class blueCar(car):
        walkRight = [pygame.image.load('bluecarright1.png'), pygame.image.load('bluecarright2.png'), pygame.image.load('bluecarright1.png'), pygame.image.load('bluecarright2.png'), pygame.image.load('bluecarright1.png'), pygame.image.load('bluecarright2.png'), pygame.image.load('bluecarright1.png'), pygame.image.load('bluecarright2.png')]
        walkLeft = [pygame.image.load('bluecarleft1.png'), pygame.image.load('bluecarleft2.png'), pygame.image.load('bluecarleft1.png'), pygame.image.load('bluecarleft2.png'), pygame.image.load('bluecarleft1.png'), pygame.image.load('bluecarleft2.png'), pygame.image.load('bluecarleft1.png'), pygame.image.load('bluecarleft2.png')]

    class Conv(car):
        walkRight = [pygame.image.load('convright1.png'), pygame.image.load('convright2.png'), pygame.image.load('convright1.png'), pygame.image.load('convright2.png'), pygame.image.load('convright1.png'), pygame.image.load('convright2.png'), pygame.image.load('convright1.png'), pygame.image.load('convright2.png')]
        walkLeft = [pygame.image.load('convleft1.png'), pygame.image.load('convleft2.png'), pygame.image.load('convleft1.png'), pygame.image.load('convleft2.png'), pygame.image.load('convleft1.png'), pygame.image.load('convleft2.png'), pygame.image.load('convleft1.png'), pygame.image.load('convleft2.png')]

    class greenVan(car):
        walkRight = [pygame.image.load('greenvanright1.png'), pygame.image.load('greenvanright2.png'), pygame.image.load('greenvanright1.png'), pygame.image.load('greenvanright2.png'), pygame.image.load('greenvanright1.png'), pygame.image.load('greenvanright2.png'), pygame.image.load('greenvanright1.png'), pygame.image.load('greenvanright2.png')]
        walkLeft = [pygame.image.load('greenvanleft1.png'), pygame.image.load('greenvanleft2.png'), pygame.image.load('greenvanleft1.png'), pygame.image.load('greenvanleft2.png'), pygame.image.load('greenvanleft1.png'), pygame.image.load('greenvanleft2.png'), pygame.image.load('greenvanleft1.png'), pygame.image.load('greenvanleft2.png')]

    class whiteVan(car):
        walkRight = [pygame.image.load('bluevanright1.png'), pygame.image.load('bluevanright2.png'), pygame.image.load('bluevanright1.png'), pygame.image.load('bluevanright2.png'), pygame.image.load('bluevanright1.png'), pygame.image.load('bluevanright2.png'), pygame.image.load('bluevanright1.png'), pygame.image.load('bluevanright2.png')]
        walkLeft = [pygame.image.load('bluevanleft1.png'), pygame.image.load('bluevanleft2.png'), pygame.image.load('bluevanleft1.png'), pygame.image.load('bluevanleft2.png'), pygame.image.load('bluevanleft1.png'), pygame.image.load('bluevanleft2.png'), pygame.image.load('bluevanleft1.png'), pygame.image.load('bluevanleft2.png')]

    class Limo(car):
        walkRight = [pygame.image.load('limoright1.png'), pygame.image.load('limoright2.png'), pygame.image.load('limoright1.png'), pygame.image.load('limoright2.png'), pygame.image.load('limoright1.png'), pygame.image.load('limoright2.png'), pygame.image.load('limoright1.png'), pygame.image.load('limoright2.png')]
        walkLeft = [pygame.image.load('limoleft1.png'), pygame.image.load('limoleft2.png'), pygame.image.load('limoleft1.png'), pygame.image.load('limoleft2.png'), pygame.image.load('limoleft1.png'), pygame.image.load('limoleft2.png'), pygame.image.load('limoleft1.png'), pygame.image.load('limoleft2.png')]

    class yellowBus(car):
        walkRight = [pygame.image.load('yellowbusright1.png'), pygame.image.load('yellowbusright2.png'), pygame.image.load('yellowbusright1.png'), pygame.image.load('yellowbusright2.png'), pygame.image.load('yellowbusright1.png'), pygame.image.load('yellowbusright2.png'), pygame.image.load('yellowbusright1.png'), pygame.image.load('yellowbusright2.png')]
        walkLeft = [pygame.image.load('yellowbusleft1.png'), pygame.image.load('yellowbusleft2.png'), pygame.image.load('yellowbusleft1.png'), pygame.image.load('yellowbusleft2.png'), pygame.image.load('yellowbusleft1.png'), pygame.image.load('yellowbusleft2.png'), pygame.image.load('yellowbusleft1.png'), pygame.image.load('yellowbusleft2.png')]
        
    class timer(object):
        def draw(win):
            countdownlist = "30"
            countdownlist = int(countdownlist)
            countdownlist = countdownlist - 1
            countdownlist = str(countdownlist)
            time.sleep(1)
            if countdownlist == "0":
                menu()
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render(countdownlist, True, (255,50,50))
            win.blit(text, (50,50))
            
    def spriteLOAD():
        win.blit(bg, (0,0))
        nestsprite.draw(win)
        chicken.draw(win)
        pointcount.draw(win)
        eggsprite.draw(win)

        
        carList = [RedCar, WhiteBus, BlueCar, YellowConv, GreenVan, WhiteVan, BlackLimo, YellowBus]
    
        for i in range(0,8):
            carGen = random.choice(carList)
            carGen.draw(win)
            carList.pop(carList.index(carGen))
        win.blit(overlay, (0,0))
        pygame.display.update()

    def fadegame(): 
        fade = pygame.Surface((1000, 1000))
        fade.fill((0,0,0))
        for alpha in range(0, 50):
            fade.set_alpha(alpha)
            win.blit(fade, (0,0))
            pygame.display.update()
            pygame.time.delay(5)
            
    usernameCheckSTR = ''.join(map(str, usernameCheck))
    c.execute("SELECT level FROM accounts WHERE username = (?)", (usernameCheckSTR,))
    levelDB = c.fetchone()
    chicken = player(random.randint(0,550), 550, 34, 44, levelDB[0])
    eggsprite = egg(random.randint(10, 550), 30, 16, 18)
    nestsprite = nest(random.randint(10, 550), 560, 66, 26)
    pointcount = textgen(point)

    #obst_clsn_avdr = [-1500, -1250, -1000, -750, -500, -250, -100] 
    RedCar = redCar([['65', '265', '420'], ['125','325', '470']], -100, 86, 33, 1505)   
    WhiteBus = whiteBus([['65', '265', '420'], ['125','325', '470']], -215, 110, 41, 1390)
    BlueCar = blueCar([['65', '265', '420'], ['125','325', '470']], -330, 86, 33, 1275)
    YellowConv = Conv([['65', '265', '420'], ['125','325', '470']], -445, 86, 33, 1160)
    GreenVan = greenVan([['65', '265', '420'], ['125','325', '470']], -560, 86, 33, 1045)
    WhiteVan = whiteVan([['65', '265', '420'], ['125','325', '470']], -675, 78, 32, 930)
    BlackLimo = Limo([['65', '265', '420'], ['125','325', '470']], -790, 110, 33, 915)
    YellowBus = yellowBus([['65', '265', '420'], ['125','325', '470']], -905, 102, 41 , 700)

    
    
    #road coordinates = 65, 125, 325, 265, 420, 470
    timer = 27
    run = True
    global countercar1
    while run:
        #27 ticks = 1 second
        clock.tick(timer)

        if chicken.hitbox[1] < eggsprite.hitbox[1] + eggsprite.hitbox[3] and chicken.hitbox[1] + chicken.hitbox[3] > eggsprite.hitbox[1]:
                if chicken.hitbox[0] + chicken.hitbox[2] > eggsprite.hitbox[0] and chicken.hitbox[0] < eggsprite.hitbox[0] + eggsprite.hitbox[2]:
                    eggsprite.x = chicken.x + 10
                    eggsprite.y = chicken.y + 10
                    
        if nestsprite.hitbox[1] < eggsprite.hitbox[1] + eggsprite.hitbox[3] and nestsprite.hitbox[1] + nestsprite.hitbox[3] > eggsprite.hitbox[1]:
                if nestsprite.hitbox[0] + nestsprite.hitbox[2] > eggsprite.hitbox[0] and nestsprite.hitbox[0] < eggsprite.hitbox[0] + eggsprite.hitbox[2]:
                    pointcount.point += 1
                    eggsprite.x = random.randint(10,650)
                    eggsprite.y = 30
                    

        for countercar in range(0,8):
            carList = [RedCar, WhiteBus, BlueCar, YellowConv, GreenVan, WhiteVan, BlackLimo, YellowBus]
            
            if chicken.hitbox[1] < carList[countercar].hitbox[1] + carList[countercar].hitbox[3] and chicken.hitbox[1] + chicken.hitbox[3] > carList[countercar].hitbox[1]:
                if chicken.hitbox[0] + chicken.hitbox[2] > carList[countercar].hitbox[0] and chicken.hitbox[0] < carList[countercar].hitbox[0] + carList[countercar].hitbox[2]:
                    
                    chicken.collision()
        
        #For loop constantly checking through every car with every other car if there is a collision
        for countercar1 in range(0, 8):
            carList = [RedCar, WhiteBus, BlueCar, YellowConv, GreenVan, WhiteVan, BlackLimo, YellowBus]
            #Second for loop to check of countercar1 collision with countercar2
            for countercar2 in range(0, len(carList)):
                if countercar2 == countercar1:
                    continue
                
                if carList[countercar1].hitbox[1] < carList[countercar2].hitbox[1] + carList[countercar2].hitbox[3] and carList[countercar1].hitbox[1] + carList[countercar1].hitbox[3] > carList[countercar2].hitbox[1]:
                    if carList[countercar2].hitbox[0] + carList[countercar2].hitbox[2] + 50 > carList[countercar1].hitbox[0] and carList[countercar2].hitbox[0] < carList[countercar1].hitbox[0] + carList[countercar1].hitbox[2] + 50 :
                        #If collision, the car behind the car in front will slow down
                        if carList[countercar1].vel > 0:
                            if carList[countercar1].x < carList[countercar2].x:
                               
                                carList[countercar1].x -= carList[countercar2].vel
                            elif carList[countercar1].x > carList[countercar2].x:
                                carList[countercar2].x -= carList[countercar1].vel
                
                        elif carList[countercar1].vel < 0:
                            if carList[countercar1].x > carList[countercar2].x:
                                carList[countercar1].x -= carList[countercar2].vel
                            elif carList[countercar1].x < carList[countercar2].x:
                                carList[countercar2].x -= carList[countercar1].vel
                                    
                        


                        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        k = pygame.key.get_pressed()

        if k[pygame.K_LEFT] and chicken.x > 0:
            chicken.x -= chicken.vel 
            #print(chicken.x)
            chicken.left = True
            chicken.right = False
            chicken.down = False
            chicken.up = False

        
        elif k[pygame.K_RIGHT] and chicken.x < (winx - chicken.width):
            chicken.x += chicken.vel
            #print(chicken.x)
            chicken.left = False
            chicken.right = True
            chicken.down = False
            chicken.up = False


        elif k[pygame.K_UP] and chicken.y > 0:
            chicken.y -=chicken. vel
            #print(chicken.y)
            chicken.right = False
            chicken.left = False
            chicken.down = False
            chicken.up = True

        elif k[pygame.K_DOWN] and chicken.y < (winy - chicken.height):
            chicken.y += chicken.vel
            #print(chicken.y)
            chicken.right = False
            chicken.left = False
            chicken.up = False
            chicken.down = True

        #elif k[pygame.K_ESCAPE]:
            ##

        elif k[pygame.K_m]:
            chicken.level += 1
            print(chicken.level)

            
        else:
            chicken.right = False
            chicken.left = False
            chicken.down = False
            chicken.up = False
            chicken.walkCount = 0
        spriteLOAD()

        
    pygame.quit()



pygame.quit()

def endgamescreen(usernameCheck):
    pygame.init()
    clock = pygame.time.Clock()
    x = 640
    y = 607
    b = 0
    countdown = 9
    countdowntext = "Wait " + str(countdown) + " Seconds or press X to go back to menu"
    win = pygame.display.set_mode((640,607))

    

    pygame.display.set_caption('Show Text') 

    font = pygame.font.Font('freesansbold.ttf', 32)
    fontSmall = pygame.font.Font('freesansbold.ttf', 18)

    textContinue = font.render('Press Enter if you want to play again', True, (255,0,0))

    textCountdown = fontSmall.render(countdowntext, True, (255,0,0)) 
    textRectContinue = textContinue.get_rect()  
    textRectContinue.center = (x // 2, y// 2)
    textRectCountdown = textCountdown.get_rect()  
    textRectCountdown.center = (x // 2, y-500 // 2)    

    while True:
        clock.tick(27)
        countdowntext = "Wait " + str(countdown) + " Seconds or press X to go back to menu"
        win.fill((0,0,0))
        win.blit(textContinue, textRectContinue)
        win.blit(textCountdown, textRectCountdown)
        
        b += 1
        if b % 27 == 0:
            countdown = countdown - 1
            textCountdown = fontSmall.render(countdowntext, True, (255,0,0))
            pygame.display.update() 
        if countdown == -1:
            return

        
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT : 
                pygame.quit() 

        k = pygame.key.get_pressed()

        if k[pygame.K_RETURN]:
            play(usernameCheck)

        if k[pygame.K_x]:
            menu(usernameCheck)
                
        pygame.display.update()  


def QUITmidGAME():
    pygame.quit()

def menu(usernameCheck):
    pygame.init()
    run = True
    clock = pygame.time.Clock()

    win = pygame.display.set_mode((640,607))
    click = pygame.mouse.get_pressed()
    mousePosition= pygame.mouse.get_pos()
    playButtonScaled = pygame.transform.scale(pygame.image.load('play.png'),(300,100))
    play_buttonOnClick = pygame.transform.scale(pygame.image.load('playClicked.png'), (300, 100))
    settingsButtonScaled = pygame.transform.scale(pygame.image.load('settings.png'),(300,100))
    settings_buttonOnClick = pygame.transform.scale(pygame.image.load('settingsClicked.png'), (300, 100))
    quitButtonScaled = pygame.transform.scale(pygame.image.load('quit.png'),(300,100))
    quit_buttonOnClick = pygame.transform.scale(pygame.image.load('quitClicked.png'), (300,100))
    bg = pygame.image.load('background.png')
    bg2 = pygame.image.load('background2.png')
    ySCROLL = 0
    playHitbox = pygame.Rect((160,130), (300,100))
    settingsHitbox = pygame.Rect((160,240), (300,100))
    quitHitbox = pygame.Rect((160,350), (300,100))
    
    #def menuLOAD():
        #global playButton
        #global settingsButton
        #global quitButton
        #playButton = win.blit(playButtonScaled, (160,130))
        #settingsButton = win.blit(settingsButtonScaled, (160,240))
        #quitButton = win.blit(quitButtonScaled, (160,350))
        #pygame.display.update()
        
    def fade(): 
        fade = pygame.Surface((1000, 1000))
        fade.fill((0,0,0))
        for alpha in range(0, 100):
            fade.set_alpha(alpha)
            win.blit(fade, (0,0))
            pygame.display.update()
            pygame.time.delay(5)
        
            

#play domain 160-460
#play range 130-230

    while run:
        clock.tick(27)
        ySCROLL = ySCROLL+1
        win.blit(bg, (0,ySCROLL-600))
        win.blit(bg, (0,ySCROLL))
        if ySCROLL == 600:
            ySCROLL = 1
            
        playButton = win.blit(playButtonScaled, (160,130))
        settingsButton = win.blit(settingsButtonScaled, (160,240))
        quitButton = win.blit(quitButtonScaled, (160,350))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1 and playHitbox.collidepoint(event.pos):
                playButton = win.blit(play_buttonOnClick, (160,240))

                
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button ==1 and settingsHitbox.collidepoint(event.pos):
                settingsButton = win.blit(settings_buttonOnClick, (160,240))
                
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button ==1 and quitHitbox.collidepoint(event.pos):
                quitButton = win.blit(quit_buttonOnClick, (160,350))
            
            if event.type == pygame.MOUSEBUTTONUP and event.button ==1 and playHitbox.collidepoint(event.pos):
                fade()
                play(usernameCheck)
                
            elif event.type == pygame.MOUSEBUTTONUP and event.button ==1 and settingsHitbox.collidepoint(event.pos):
                print("clicked settings")
            elif event.type == pygame.MOUSEBUTTONUP and event.button ==1 and quitHitbox.collidepoint(event.pos):
                fade()
                pygame.quit()
                break
        
        
    pygame.quit()

loginsystem()
#menu()
