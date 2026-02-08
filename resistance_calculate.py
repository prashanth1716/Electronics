'''
Resistors:\n
band_resistor(colours_name).result()\n
smd_eia96(digits).results()\n
connect_resistors(values).results()
'''
import shutil,os

#colour band resistor
class band_resistor:
    '''band resistor is a old resistor calculate by colour code\n
    colours: "black", "brown", "red", "orange", "yellow", "green", \n
             "blue", "violet", "grey", "white", "gold", "silver"'''
    
    #get data
    def __init__(self,*kwarg):
        self.kwarg = kwarg  
        
    #processing 
    def calculate(self):
        '''d = digits, m = multiply, t = tolerance, tc = temperature coefficient(ppm/k), f = fail rate'''

        #colour chart
        colour_chart = {
            "black": {"d":0, "m":1, 't':0, "tc":[250,"ppm/k","U"],'f':0},
            "brown": {'d':1, "m":10, 't':[1,"F"], "tc":[100,"ppm/k","S"], "f":1},
            "red": {'d':2, 'm':100, 't':[2,"G"], "tc":[50,"ppm/k","R"], 'f':0.1},
            "orange": {'d':3, 'm':1000, 't':[0.05,'W'], "tc":[15,"ppm/k","P"], 'f':0.01},
            "yellow": {'d':4, 'm':10000, 't':[0.02,'P'], "tc":[25,"ppm/k","Q"], 'f':0.001},
            "green": {'d':5, 'm':100000, 't':[0.5,"D"], "tc":[20,"ppm/k","Z"], 'f':0},
            "blue": {'d':6, 'm':1000000, 't':[0.25,"C"], "tc":[10,"ppm/k","Z"], 'f':0},
            "violet": {'d':7, 'm':10000000, 't':[0.1,"B"], "tc":[5,"ppm/k","M"], 'f':0},
            "grey": {'d':8, 'm':100000000, 't':[0.01,"A"], "tc":[1,"ppm/k","K"], 'f':0},
            "white": {'d':9, 'm':1000000000, 't':0, "tc":0, 'f':0},
            "gold": {'d':0, 'm':0.1, 't':[5,"J"], "tc":0, 'f':0},
            "silver": {'d':0, 'm':0.01, 't':[10,"K"], "tc":0, 'f':0},
        }  #if 3 band reisistor there tolerance 20,(M)

        length = len(self.kwarg)   #length of given user colour list
        i,d,m,t,tc,f = 0,'',0,0,0,0     #varables for output
        #list of colours
        colour_list = ["black", "brown", "red", "orange", "yellow", "green",
                       "blue", "violet", "grey", "white", "gold", "silver"]
        
        #filter and conditions processing 
        if length >= 3 and length <= 6: 
            if length == 3: #3 band resistor
                for c in self.kwarg:
                    i = i + 1
                    if c in colour_list:  #filter
                        if i != 3: d += str(colour_chart[c]["d"])
                        elif i == 3: m = colour_chart[c]["m"]
                    else: return f"E: not found colour: {c}"  #if colour error
                d = int(d)
                return {"ohm's" :d*m, "tolerance":[20,"M"]}  #return value
            
            elif length == 4: # 4band resistor
                for c in self.kwarg:
                    i = i + 1
                    if c in colour_list:   #filter
                        if i >= 1 and i < 3: d += str(colour_chart[c]["d"])
                        elif i == 3: m = colour_chart[c]["m"]
                        elif i == 4: t = colour_chart[c]["t"]
                    else: return f"E: not found colour: {c}"  #if colour error

                d = int(d)
                return {"ohm's": (d*m),"tolerance": t}

            elif length == 5:   #5 band resistor
                for c in self.kwarg:
                    i = i + 1
                    if c in colour_list:   #filter
                        if i >= 1 and i < 4: d += str(colour_chart[c]["d"])
                        elif i == 4: m = colour_chart[c]["m"]
                        elif i == 5: t = colour_chart[c]["t"]
                    else: return f"E: not found colour: {c}"  #if colour error

                d = int(d)
                return {"ohm's": (d*m),"tolerance": t}
       
            elif length == 6:   #6 band resistor
                for c in self.kwarg:
                    i = i + 1
                    if c in colour_list:   #filter
                        if i >= 1 and i < 4: d += str(colour_chart[c]["d"])
                        elif i == 4: m = colour_chart[c]["m"]
                        elif i == 5: t = colour_chart[c]["t"]
                        elif i == 6: tc = colour_chart[c]["tc"]
                    else: return f"E: not found colour: {c}"  #if colour error

                d = int(d)
                return {"ohm's": (d*m),"tolerance": t, "temperature_coefficient": tc}
            
        else:
            return f"E: there is no band resistors of {len(self.kwarg)}"
    
    #result
    def result(self):

        def number_to_words(num):
            if num >= 1_000_000_000_000_000_000: return f"{num/1_000_000_000_000_000_000:.2f}E" #exa
            elif num >= 1_000_000_000_000_000: return f"{num/1_000_000_000_000_000:.2f}P" #peta
            elif num >= 1_000_000_000_000: return f"{num/1_000_000_000_000:.2f}T" #Tera
            elif num >= 1_000_000_000: return f"{num/1_000_000_000:.2f}G" #Giga
            elif num >= 1_000_000: return f"{num/1_000_000:.2f}M"  #Mega
            elif num >= 1_000: return f"{num/1_000:.2f}K" #kilo
            else: return str(num) #num
        
        data = self.calculate()

        colour_list = {'black':"\033[30m",
        'brown':"\033[30m", 'red':"\033[31m",
        'green':"\033[32m", 'yellow':"\033[33m",
        'orange':"\033[33m", 'gold':"\033[33m",
        'blue':"\033[34m", 'violet':"\033[35m",
        'cyan':"\033[36m", 'white':"\033[37m",
        'grey':"\033[37m", "silver":"\033[37m"}

        if isinstance(data,str):  #if any error
            print("\033[1m\033[31m", data , "\033[0m")

        else:  #without errors

            
            print("#"*40, "\n")  #print #'s

            '''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            >>>>>>> resistor design >>>>>>>>>>>>>
            >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''
            if len(self.kwarg) == 3:
                print(f"--- {colour_list[self.kwarg[0]]}| {colour_list[self.kwarg[1]]}|   {colour_list[self.kwarg[2]]}| \033[0m---")

            elif len(self.kwarg) == 4:
                print(f"--- {colour_list[self.kwarg[0]]}| {colour_list[self.kwarg[1]]}| {colour_list[self.kwarg[2]]}|   {colour_list[self.kwarg[3]]}| \033[0m---")

            elif len(self.kwarg) == 5:
                print(f"--- {colour_list[self.kwarg[0]]}| {colour_list[self.kwarg[1]]}| {colour_list[self.kwarg[2]]}| {colour_list[self.kwarg[3]]}|   {colour_list[self.kwarg[4]]}| \033[0m---")

            elif len(self.kwarg) == 6:
                print(f"--- {colour_list[self.kwarg[0]]}| {colour_list[self.kwarg[1]]}| {colour_list[self.kwarg[2]]}| {colour_list[self.kwarg[3]]}| {colour_list[self.kwarg[4]]}|   {colour_list[self.kwarg[5]]}| \033[0m---")


            ohm = number_to_words(data["ohm's"])
            tolerance = data["tolerance"]

            print("\n\033[1m\033[36m", f"{ohm} Ω", end='') #ohm's print

            try: 
                print(f" +{tolerance[0]}%({tolerance[1]})", end='') #tolerance print
            except TypeError:
                pass

            try: 
                temp_coef = data["temperature_coefficient"]
                print(f" {temp_coef[0]}{temp_coef[1]}({temp_coef[2]})", end='')  #temp coef print
            except: pass

            print("\033[0m\n\n", "#"*39, "\n")  #print #'s

            return data

#smd & eia-96
class smd_eia96:
    """smd = [0-9, 'R'], 3 or 4 digits 'R' be only one on one resistor\n
    eia-96 = [01 - 96 ] and ["z", "y", "r", "x", "s", 'a', 'B', 'h', 'c', 'd', 'e', 'f'] \n
    use only last digit a string"""
    #user input
    def __init__(self,*kwarg):
        self.kwarg = kwarg

    #processing data
    def calculate(self):
        length = len(self.kwarg)  #length
        characters = []
        self.strings,self.eia_word,j = 0,0,0
        answer = ""
        eia_96_numbers = {"01":100, "02":102, "03":105, "04":107, "05":110, "06":113, "07":115, '08':118, "09":121, "10":124,
                          "11":127, "12":130, "13":133, "14":137, "15":140, "16":143, "17":147, "18":150, "19":154, "20":158,
                          "21":162, "22":165, "23":169, "24":174, "25":178, "26":182, "27":187, "28":191, "29":196, "30":200,
                          "31":205, "32":210, "33":215, "34":221, "35":226, "36":232, "37": 237, "38":243, "39":249, "40":255,
                          "41":261, "42":267, "43":274, "44":280, "45":287, "46":294, "47":301, "48":309, "49":316, "50":324,
                          "51":332, "52":340, "53":348, "54":357, "55":365, "56":374, "57":383, "58":392, "59":402, "60":412,
                          "61":422, "62":432, "63":442, "64":453, "65":463, "66":475, "67":487, "68":499, "69":511, "70":523,
                          "71":536, "72":549, "73":562, "74":576, "75":590, "76":604, "77":619, "78":634, "79":649, "80":665,
                          "81":681, "82":698, "83":715, "84":732, "85":750, "86":768, "87":787, "88":806, "89":825, "90":845,
                          "91":866, "92":887, "93":909, "94":931, "95":953, "96":976}
        
        eia_96_letters = {"z":0.001, "y":0.01, "r":0.01, "x": 0.1, "s":0.1,'a':1,
                          'B':10, 'h':10, 'c': 100, 'd':1000, 'e':10000, 'f':100000}
   
        if length == 3:
            #filter
            f,s,t = self.kwarg[0], self.kwarg[1], self.kwarg[2]
            #frist digit
            if isinstance(f,(int,str)):
                if len(str(f)) == 1:
                    try: f = int(f) #if int accept
                    except ValueError:
                        if f.upper() == 'R':
                            self.strings = self.strings+1     
                            f = str("0.")
                        else: return f"E: use 'R' or 1-0 if smd resistor calculation not '{f}'"  #if not a number or r in frist digit
                else: return f"E: use single digit only not '{f}'" #if multiple digits error
            else: return f"E: use only string or int not '{f}' " #if it not str or int

            #second digit
            if isinstance(s,(int,str)):
                if len(str(s)) == 1:
                    try: s = int(s) #if int accept
                    except ValueError:
                        if self.strings == 0:
                            if s.upper() == 'R':
                                self.strings = self.strings+1     
                                s = str(".")
                            else: return f"E: use 'R' or 1-0 if smd resistor calculation not '{s}'"  #if not a number or r in frist digit
                        else: return f"E: In smd or eia-96 there only 1 digit string"  #if mutliple strings 
                else: return f"E: use single digit only not 0-9 or 'R' not {s}'" #if multiple digits error
            else: return f"E: use only string or int not '{s}' " #if it not str or int
            
            #thrid
            if isinstance(t,(int,str)):
                if len(str(t)) == 1:
                    try: t = int(t) #if int accept
                    except ValueError:
                        if self.strings == 0:
                            for i in eia_96_letters.keys():
                                if t.lower() == i:
                                    t = eia_96_letters[i]
                                    self.eia_word = self.eia_word + 1
                                    break
                            if self.eia_word == 0: return f"E: con't found '{t}' in eia-96"
                        else: return f"E: In smd or eia-96 there only 1 digit string"  #if mutliple strings 
                else: return f"E: use single digit only not 0-9 or 'R' not {t}'" #if multiple digits error
            else: return f"E: use only string or int not '{t}' " #if it not str or int

            #solutions
            if self.strings == 0 and self.eia_word == 0:  #pure smd 
                answer = int(str(f) + str(s)) * (10 ** t)
                return {"ohm":answer,"tolerance": 5} 
            elif self.strings == 1:  #with "r"
                answer = str(f) + str(s) + str(t)
                return {"ohm":answer, "tolerance": 5}
            elif self.eia_word == 1:  #eia-96
                try: answer = eia_96_numbers[str(f)+str(s)] 
                except KeyError: return f"E: eia-96 use only 1-96 not '{str(f)+str(s)}'"
                return {"ohm":answer*t, "tolerance":1}

        elif length == 4:  #if smd 4 character resistor
            #filter

            for i in self.kwarg:
                if isinstance(i,(int,str)):  #1 character
                    try: characters.append(int(i))
                    except ValueError:
                        self.strings = self.strings + 1
                        f = i.upper()
                        if f == "R": characters.append(".")
                        else: return f"E: 4digit smd resistor not use '{f}'" #if character is invaild error
                else: return f"E: use only int or str not 'Float'"  #if float error

            #if zero strings in given data
            if self.strings == 0:
                for i in characters:
                    j = j + 1
                    if j == 4: pass
                    else: answer += str(i)

                answer = int(answer) * (10 ** i)

            #if one "R" in given data
            elif self.strings == 1:
                for i in characters:
                    j = j + 1
                    if i =='.':
                        if j == 1: answer += "0."
                        elif j == 4: pass
                        else: answer += "."
                    else: answer += str(i)
            
            #if mutliple 'R' letters in given data
            elif self.strings > 1: return f"E: 4digit resistor use 1character and 3integers ex: '[1R23]' not {characters}"  

            return {"ohm":answer,"tolerance":1}

        else: return f"E: no smd resistor with {self.kwarg}"  #error in length

    #result
    def result(self):
        #number to words
        def number_to_words(num):
            if num >= 1_000_000_000_000_000_000: return f"{num/1_000_000_000_000_000_000:.2f}E" #exa
            elif num >= 1_000_000_000_000_000: return f"{num/1_000_000_000_000_000:.2f}P" #peta
            elif num >= 1_000_000_000_000: return f"{num/1_000_000_000_000:.2f}T" #Tera
            elif num >= 1_000_000_000: return f"{num/1_000_000_000:.2f}G" #Giga
            elif num >= 1_000_000: return f"{num/1_000_000:.2f}M"  #Mega
            elif num >= 1_000: return f"{num/1_000:.2f}K" #kilo
            else: return str(num) #num

        #varables
        data = self.calculate()
        self.kwarg = list(self.kwarg)
        length = len(self.kwarg)
        j=0

        #filter for upper character
        for i in self.kwarg:
            try: self.kwarg[j] = int(self.kwarg[j])
            except: self.kwarg[j] = str(self.kwarg[j]).upper()
            j += 1

        #styling
        if length == 3:
            try:
                if self.eia_word == 1: print("\033[1m\033[36m"+"Eia-96"+"\033[0m")
                else: print("\033[1m\033[36m"+"3 Digit"+"\033[0m")
                try:data['ohm'] = number_to_words(data['ohm']) #filter num to word
                except: pass
                print("","-"*9,"\n", f"|| {self.kwarg[0]}{self.kwarg[1]}{self.kwarg[2]} ||\n", "-"*9 )
                print("\033[1m\033[32m",f"{data['ohm']} Ω ", f"+{data['tolerance']}%\033[0m")
            except: print("\033[1m\033[31m",data,"\033[0m")
            
        elif length == 4:
            try:
                print("\033[1m\033[36m"+"4 Digit"+"\033[0m")
                try:data['ohm'] = number_to_words(data['ohm']) #filter num to word
                except: pass
                print("","-"*10,"\n", f"|| {self.kwarg[0]}{self.kwarg[1]}{self.kwarg[2]}{self.kwarg[3]} ||\n", "-"*10 )
                print("\033[1m\033[32m",f"{data['ohm']} Ω ", f"+{data['tolerance']}%\033[0m")
            except: print("\033[1m\033[31m",data,"\033[0m")
            
        return data 

#parallel and series
class connect_resistors:

    """cal_type use frist charater 'p' and 's' or 'parallel' or 'series'"""

    #user data input
    def __init__(self,cal_type="parallel"or"series",*kwargs):
        self.cal_type = cal_type
        self.kwargs = kwargs

    #processing data
    def calculate(self):

        #varables
        r = 0
        resistors_value = []
        #word to number
        def word_to_nmber(data:str):
            try: return int(data)  #if int
            except:
                try: return float(data) #if float
                except:
                    data = data.lower() #lower text
                    if data.endswith("k"): return float(data[:-1]) * 1_000   #kilo
                    elif data.endswith("m"): return float(data[:-1]) * 1_000_000   #mega
                    elif data.endswith("g"): return float(data[:-1]) * 1_000_000_000   #giga
                    elif data.endswith("t"): return float(data[:-1]) * 1_000_000_000_000   #tera
                    elif data.endswith("p"): return float(data[:-1]) * 1_000_000_000_000_000   #peta
                    elif data.endswith("e"): return float(data[:-1]) * 1_000_000_000_000_000_000   #exa
                    else: return f"E:word to number error '{data}'"  #error

        #filter
        #cal_type
        self.cal_type = "".join(self.cal_type.split()) #remove backspaces and newlines
        if self.cal_type.startswith("p"):  self.cal_type = "parallel"  #if frist letter p then it is parallel
        elif self.cal_type.startswith("s"): self.cal_type = "series"  #if frist letter s then it is series
        else: return f"E use 'p','s','parallel' or 'series' not {self.cal_type}"

        #numbers
        for i in self.kwargs:
            data = word_to_nmber(i)    
            if isinstance(data,str): return data   #if error in given number
            resistors_value.append(data)

        #parallel
        if self.cal_type == "parallel":
            for i in resistors_value:
                r += 1/i
            return {"ohm":round(1/r,2)}
        
        #series
        elif self.cal_type == "series":
            for i in resistors_value:
                r += i
            return {'ohm':round(r,2)}

    #result and styling
    def result(self):

        #varables
        try: 
            data = self.calculate()['ohm']
        except:
            print("\033[1m\033[31m",self.calculate(), "\033[0m")  #if error
            return self.calculate()

        #number to words
        def number_to_words(num):
            if num >= 1_000_000_000_000_000_000: return f"{num/1_000_000_000_000_000_000:.2f}E" #exa
            elif num >= 1_000_000_000_000_000: return f"{num/1_000_000_000_000_000:.2f}P" #peta
            elif num >= 1_000_000_000_000: return f"{num/1_000_000_000_000:.2f}T" #Tera
            elif num >= 1_000_000_000: return f"{num/1_000_000_000:.2f}G" #Giga
            elif num >= 1_000_000: return f"{num/1_000_000:.2f}M"  #Mega
            elif num >= 1_000: return f"{num/1_000:.2f}K" #kilo
            else: return str(num) #num

        #filter
        data = number_to_words(data)

        if self.cal_type == "parallel":  #print parallel connection
            print("\033[1m\033[33m parallel connection ")
            print("\033[1m\033[33m |-/\/\/\-|\n"*3)
        elif self.cal_type == "series":  #print series connections
            print("\033[1m\033[33m series connection ")
            print('\033[1m\033[33m',"-/\/\/\-"*3)

        print("\033[1m\033[32m",data, "Ω\033[0m\n")  #print data


        #return
        return self.calculate()

if __name__ == "__main__":
    bold_text = "\033[1m"
    black ="\033[30m"
    red ="\033[31m"
    green = "\033[32m" 
    yellow = "\033[33m"
    blue = "\033[34m"
    violet = "\033[35m"
    cyan = "\033[36m"
    white ="\033[37m"
    reset = "\033[0m"

    #varables
    get = 0
    quit = False
    error = ""
    size = shutil.get_terminal_size() #get size of terminal
    c,r = size.columns, size.lines   #coloums and rows
    text = "Resistor calculation" #text for print headline
    r_space = round((r/2.5)/2 - text.count("s")+1)  #rows calculation
    

    #functions
    #band resistor styling
    def band_styling():
        global quit
        data = []
        text = "band resistor & colour code calculation".upper()
        os.system("clear")   #clean screen

        print(f"{bold_text}{yellow}+" + "-"*(c-2) + "+")  #headline
        for i in range(r_space): print("|" + " "*(c-2) + "|")  #row print
        print(f"|{violet}"+ text.center(c-2)+f"{yellow}|")       #text print
        for i in range(r_space): print("|" + " "*(c-2) + "|")  #row print
        print("+" + "-"*(c-2) + f"+{reset}")  #footline

        #main loop
        while True:
            try:
                try:
                    get = int(input(f"{bold_text}{cyan}"+"\n1 3band resistor \n2 4band resistor \n3 5band resistor \n4 6band resistor \n5 back \n6 quit or crtl + c,crtl + D \nEnter: ".title() + f"{yellow}"))
                except ValueError:
                    print(f"{red}" + "\nenter only numbers 1-6".title())
                except KeyboardInterrupt:
                    print(f"{violet}" + "\n\nThank you!!!\n".title() + f"{reset}")
                    quit = True
                    break
                except EOFError: 
                    quit = True
                    print(f"{violet}" + "\n\nThank you!!!\n".title() + f"{reset}")
                    break
                
                #3band resistor
                if get == 1: 
                    print(f'{yellow}"black", "brown", "red", "orange", "yellow", "green","blue", "violet", "grey", "white", "gold","silver"{cyan}')
                    #loop for get data form user
                    for i in range(1,4):
                        data.append(input(f"{cyan}Enter {i} colour :{yellow} "))
                        
                    print(reset)
                    band_resistor(*data).result() #calculate
                    data = []

                #4band resistor
                elif get == 2:
                    print(f'{yellow}"black", "brown", "red", "orange", "yellow", "green","blue", "violet", "grey", "white", "gold","silver"{cyan}')
                    #loop for get data form user
                    for i in range(1,5):
                        data.append(input(f"{cyan}Enter {i} colour :{yellow} "))
                        
                    print(reset)
                    band_resistor(*data).result() #calculate
                    data = []

                #5band resistor
                elif get == 3:
                    print(f'{yellow}"black", "brown", "red", "orange", "yellow", "green","blue", "violet", "grey", "white", "gold","silver"{cyan}')
                    #loop for get data form user
                    for i in range(1,6):
                        data.append(input(f"{cyan}Enter {i} colour :{yellow} "))
                        
                    print(reset)
                    band_resistor(*data).result() #calculate
                    data = []

                #6band resistor
                elif get == 4:
                    print(f'{yellow}"black", "brown", "red", "orange", "yellow", "green","blue", "violet", "grey", "white", "gold","silver"{cyan}')
                    #loop for get data form user
                    for i in range(1,7):
                        data.append(input(f"{cyan}Enter {i} colour :{yellow} "))
                        
                    print(reset)
                    band_resistor(*data).result() #calculate
                    data = []
                
                #back
                elif get == 5:break

                #quit
                elif get == 6:
                    quit = True
                    print(f"{violet}" + "\n\nThank you!!!\n".title() + f"{reset}")
                    break
                
                #wrong digit
                else: print(f"{red}Enter valid number?{reset}")
            except KeyboardInterrupt: break
            except EOFError: break
    
    #sim or eia-96 styling
    def smd_styling():
        text = "SMD & EIA-96 calculation".upper()
        global quit
        data = []
        os.system("clear")   #clean screen

        print(f"{bold_text}{yellow}+" + "-"*(c-2) + "+")  #headline
        for i in range(r_space): print("|" + " "*(c-2) + "|")  #row print
        print(f"|{violet}"+ text.center(c-2)+f"{yellow}|")       #text print
        for i in range(r_space): print("|" + " "*(c-2) + "|")  #row print
        print("+" + "-"*(c-2) + f"+{reset}")  #footline

        #main loop
        while True:
            try:
                print(f"{yellow}\nsmd = [0-9, 'R'], 3 or 4 digits \neia-96 = 1st digit [0-9], 2nd[0-9] if 1st digit[9] then 2nd digit [0-6] only and 3rd ['z', 'y', 'r', 'x', 's', 'a', 'B', 'h', 'c', 'd', 'e', 'f']{reset}")
                try:
                    get = int(input(f"{bold_text}{cyan}"+"\n1 3 digit calculation \n2 4 digit calculation \n3 back \n4 quit or crtl + c,crtl + D \nEnter: ".title() + f"{yellow}"))
                except ValueError:
                    print(f"{red}" + "\nenter only numbers 1-3".title())
                except KeyboardInterrupt:
                    print(f"{violet}" + "\n\nThank you!!!\n".title() + f"{reset}")
                    quit = True
                    break
                except EOFError: 
                    quit = True
                    print(f"{violet}" + "\n\nThank you!!!\n".title() + f"{reset}")
                    break
                    
                #calculation
                #3digit
                if get == 1: 
                        for i in range(1,4):
                            data.append(input(f"{cyan}Enter {i} digit : {yellow}"))
                            
                        smd_eia96(*data).result()  #calculation
                        data = []

                    #4digit
                elif get == 2: 
                    for i in range(1,5):
                        data.append(input(f"{cyan}Enter {i} digit : {yellow}"))

                    smd_eia96(*data).result()  #calculation
                    data = []

                #back
                elif get == 3: break
                #quit
                elif get == 4:
                        quit = True
                        print(f"{violet}" + "\n\nThank you!!!\n".title() + f"{reset}")
                        break
                #wrong digit 
                else: print(f"{red}Enter valid number?{reset}")
            except KeyboardInterrupt: break
            except EOFError: break
    
    #parallel or series styling
    def parallel_styling():
        text = "parallel and series calculation".upper()
        global quit
        j = 1
        data = []
        os.system("clear")   #clean screen

        print(f"{bold_text}{yellow}+" + "-"*(c-2) + "+")  #headline
        for i in range(r_space): print("|" + " "*(c-2) + "|")  #row print
        print(f"|{violet}"+ text.center(c-2)+f"{yellow}|")       #text print
        for i in range(r_space): print("|" + " "*(c-2) + "|")  #row print
        print("+" + "-"*(c-2) + f"+{reset}")  #footline

        #main loop
        while True:
            try:
                get = int(input(f"{bold_text}{cyan}"+"\n1 parallel connection \n2 series connection \n3 back \n4 quit or crtl + c,crtl + D \nEnter: ".title() + f"{yellow}"))
            except ValueError:
                print(f"{red}" + "\nenter only numbers 1-4".title())
            except KeyboardInterrupt:
                print(f"{violet}" + "\n\nThank you!!!\n".title() + f"{reset}")
                quit = True
                break
            except EOFError: 
                quit = True
                print(f"{violet}" + "\n\nThank you!!!\n".title() + f"{reset}")
                break

            #parallel
            if get == 1: 
                #processing
                print(f"{yellow} enter 'ok' or click + C, click + D for answer")
                try:
                    while True:
                        t_data = input(f"{cyan}Enter {j} resistor value: {yellow}")
                        
                        j = j + 1
                        if t_data == "ok": 
                            print(reset)
                            if len(data) == 0: data.append(1) #if data empty
                            connect_resistors("parallel",*data).result()  #calculate
                            data =[]
                            j = 1
                            break

                        else: data.append(t_data)

                except KeyboardInterrupt:
                    print(reset)
                    if len(data) == 0: data.append(1) #if data empty
                    j = 1
                    connect_resistors("parallel",*data).result()  #calculate
                    data =[]
                except EOFError:
                    print(reset)
                    if len(data) == 0: data.append(1) #if data empty
                    j = 1
                    connect_resistors("parallel",*data).result()  #calculate
                    data =[]

            #series
            elif get == 2:
                #processing
                print(f"{yellow} enter 'ok' or click + C, click + D for answer")
                try:
                    while True:
                        t_data = input(f"{cyan}Enter {j} resistor value: {yellow}")
                        
                        j = j + 1
                        if t_data == "ok": 
                            print(reset)
                            if len(data) == 0: data.append(1) #if data empty
                            connect_resistors("series",*data).result()  #calculate
                            j = 1
                            data =[]
                            break

                        else: data.append(t_data)

                except KeyboardInterrupt:
                    print(reset)
                    if len(data) == 0: data.append(1) #if data empty
                    j = 1
                    connect_resistors("series",*data).result()  #calculate
                    data =[]

                except EOFError:
                    print(reset)
                    if len(data) == 0: data.append(1) #if data empty
                    j = 1
                    connect_resistors("series",*data).result()  #calculate
                    data =[]

            #back
            elif get == 3: break

            #quit
            elif get == 4: 
                print(f"{violet}" + "\n\nThank you!!!\n".title() + f"{reset}")
                quit = True
                break
            
            #wrong digit
            else: print(f"{red}Enter valid number?{reset}")

    #main program
    while True:
        if quit == True: break   #quit if quit in functions
        os.system("clear")   #clean screen

        print(f"{bold_text}{yellow}+" + "-"*(c-2) + "+")  #headline
        for i in range(r_space): print("|" + " "*(c-2) + "|")  #row print
        print(f"|{violet}"+ text.center(c-2)+f"{yellow}|")       #text print
        for i in range(r_space): print("|" + " "*(c-2) + "|")  #row print
        print("+" + "-"*(c-2) + f"+{reset}")  #footline

        if len(error) != 0: 
            print(error)
            error = ""

        #get data form user
        try:
            get = int(input(f"{bold_text}{cyan}\n1 colour code calculation \n2 smd & eia-96 calculation \n3 parallel or series calculation \n4, ctrl +C, ctrl +D for quit\nEnter: {yellow}"))
        except ValueError:
            print(f"{red}" + "\nenter only numbers 1-4")
        except KeyboardInterrupt:
            print(f"{violet}" + "\n\nThank you!!!\n" + f"{reset}")
            break
        except EOFError: 
            print(f"{violet}" + "\n\nThank you!!!\n" + f"{reset}")
            break
        
        #checking
        if get == 1: band_styling()  #enter band resistor function
        elif get == 2: smd_styling()  #enter smd & eia-96 resistor function
        elif get == 3:parallel_styling()  #enter parallel & series resistor function
        elif get == 4:      
            print(f"{violet}" + "\nThank you!!!\n" + f"{reset}")   #Quit
            break
        else: error = f"{red}Enter valid number?{reset}" #wrong digit enter by user
