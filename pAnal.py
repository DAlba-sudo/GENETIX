from ChromoV2 import Chromosome, Population
import os

def main():

    os.system('clear')

    while True:
        try:
            user_input = int(input("What would you like to do?\n(1) Analyze Fit\n(2) Analyze Gene Avg\n(3) Migrate Data\n>>"))
            break
        except ValueError:
            pass
    
    if(user_input == 1):
        while True:
            try:
                user_input = int(input("Would you like this with gen or without?\n 1) With Gen\n 2) Without\n>>"))
                break
            except ValueError:
                pass
        for gen in range(len(totalGen)):
            current_gen = totalGen[gen]
            current_gen_fit_sum = 0
            current_gen_avg = 0
            for ind in range(len(current_gen)):
                current_ind = current_gen[ind]
                current_gen_fit_sum += current_ind.getFit()
            
            current_gen_avg = current_gen_fit_sum / (len(current_gen))
            if(user_input == 1):
                print("%s, %s," % (gen, current_gen_avg))
            else:
                print("%s," % (current_gen_avg))

    
    elif(user_input == 2):
        while True:
            try:
                user_input = int(input("Would you like this with gen or without?\n 1) With Gen\n 2) Without\n>>"))
                break
            except ValueError:
                pass
        print("generation, gene, avg,")
        for gen in range(len(totalGen)):
            current_gen = totalGen[gen]
            
            gene_sum = {
                
            }

            for itm in range(len(gene_key)):
                c_itm = gene_key[itm]
                gene_sum[c_itm] = 0

            for ind in range(len(current_gen)):
                current_ind = current_gen[ind]
                for key in current_ind.GENES:
                    gene_sum[key] += current_ind.displayGene(key)

            tempArr = []
            for key in gene_sum:
                current_gene_avg = gene_sum[key] / (len(current_gen))
                tempArr.append(current_gene_avg)
                # if(user_input == 1):
                #     if(gene_key[0] == key):
                #         print("%s, %s, %s," % (gen, key, current_gene_avg))
                #     else:
                #         if(gen < 10):
                #             print("   "+ "%s, %s," % (key, current_gene_avg))
                #         else:
                #             print("    "+ "%s, %s," % (key, current_gene_avg))
                # else: 
                #     if(gene_key[0] == key):
                #         print("%s, %s," % (key, current_gene_avg))
                #     else:
                #         if(gen < 10):
                #             print("%s, %s," % (key, current_gene_avg))
                #         else:
                #             print("%s, %s," % (key, current_gene_avg))
            
            print("%s, %s," % (tempArr[0], tempArr[1]))



    elif(user_input == 3):
        os.system('python pAnal.py')
    print("Collect data, press enter when done!")
    input(">>")
    
    main()

if __name__ == "__main__":

    GA = Population(80)

    rootChromo = Chromosome()
    rootChromo.line = 1
    rootChromo.addGene("qC", 30)
    rootChromo.addGene("qS", 12)
    GA.addRoot(rootChromo)

    BASE_PATH = os.path.dirname(__file__)

    os.system('clear')
    g_tempSteady = []

    gene_key = []

    for key in GA.root.GENES:
        gene_key.append(key)
    
    generation_dict = {

    }

    os.system('clear')

    target_dir = input("What is the name of your target directory?\n>>")
    target_dir = os.path.join(BASE_PATH, target_dir)

    genNUM = int(input("How many generations?\n>>"))

    os.system('clear')

    file_num = 0
    totalGen = []
    for f in range(genNUM):
        tempPop = []
        file_path = "tempSteady%s.txt" % (str(f))
        path = os.path.join(target_dir, file_path)
        GA.importChromosomeIntoArray(path, tempPop)
        totalGen.append(tempPop)
        file_num += 1

    main()