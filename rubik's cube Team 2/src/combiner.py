
final = list()
simulado = list()
class Combine:

    def sides(self, sides):
        """Join all the sides together into one single string.

        :param sides: dictionary with all the sides
        :returns: string
        """
        combined = ''
        for face in 'DBRFLU':
            combined += ''.join(sides[face])
        #print(combined)
        # Python code to convert string to list character-wise 
        def Convert(string): 
            list1=[] 
            list1[:0]=string 
            return list1 
         
        str1="ABCD"
        combined2 = Convert(combined)
        for i in combined2:
            if i == 'F':
                x = 'g'
            elif i == 'U':
                x = 'w'
            elif i == 'B':
                x = 'b'
            elif i == 'R':
                x = 'r'
            elif i == 'L':
                x = 'o'
            elif i == 'D':
                x = 'y'
            else:
                x = 'error'
            final.append(x)
        # Function to convert
        print(final)

        simulador = [final[45],final[46],final[47],final[50],final[53],final[52],final[51],final[48],final[9],final[10],final[11],final[14],final[17],final[16],final[15],final[12],final[18],final[19],final[20],final[23],final[26],final[25],final[24],final[21],final[27],final[28],final[29],final[32],final[35],final[34],final[33],final[30],final[36],final[37],final[38],final[41],final[44],final[43],final[42],final[39],final[0],final[1],final[2],final[5],final[8],final[7],final[6],final[3]]
        for i in simulador:
            if i == 'w':
                x = 0
            elif i == 'b':
                x = '1'
            elif i == 'r':
                x = '2'
            elif i == 'g':
                x = '3'
            elif i == 'o':
                x = '4'
            elif i == 'y':
                x = '5'
            else:
                x = 'error'
            simulado.append(x)
        print (simulado)
        
        def listToString(s):  
    
        # initialize an empty string 
            str1 = ""  
    
        # traverse in the string   
            for ele in s:  
                str1 += ele   
    
        # return string   
            return str1  
        
        
        # Driver code
        global rubik
        rubik = listToString(final)
        simul = listToString(simulador)

        count = 0
        with open('simulador.txt', 'w') as f:
            f.write("{int[48]}\n")
            for item in simulado[:-1]:
                f.write("    [%d]: %s\n"%(count,item))
                count = count+1
            f.write("    [47]: %s"% simulado[-1])
        
        print(rubik)

        return rubik
        
combine = Combine()

