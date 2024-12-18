import matplotlib.pyplot as plt
import os

def create_graph(name, position, x_name, x_s, y_name, y_s):
    width = 10
    height = width * (2 / 3)
    
    plt.figure(figsize=(width, height))

    plt.plot(x_s, y_s, marker='.', color='#404040', linewidth=3) 

    plt.xlabel(x_name, fontsize=15)
    plt.ylabel(y_name, fontsize=15)
    
    plt.grid(True)
    
    plt.xlim(left=0)  
    plt.ylim(bottom=0)  

    plt.xticks(x_s)  
    plt.tick_params(axis='both', which='major', labelsize=15)

    plt.gca().set_position([0.18, 0.3, 0.75, 0.65]) 

    if not os.path.exists(position):
        os.makedirs(position)

    file_pdf = os.path.join(position, name + '.pdf')
    plt.savefig(file_pdf, format="pdf")

    plt.close()