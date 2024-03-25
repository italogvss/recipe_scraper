from bs4 import BeautifulSoup
def getInfos(soup, obj):
    #Titulo
    obj.title = soup.title.text
    #Informaçoões
    infoContainer = soup.find(class_='info-recipe mb-3')
    if(infoContainer == None):
        infoContainer = soup.find(class_='info-recipe info-14 mb-3')
    itens = infoContainer.find_all("span", class_="align-middle")
    obj.portion = itens[0].text
    obj.time = itens[1].text
    #print(obj)
    
    

#Precisa tratar ingredientes extras
def getIngredients(soup, obj):
    ingredientDiv = soup.find(class_='ingredientes mt-4 mb-4')
    h2List = ingredientDiv.find_all('h2')
    list = []

    #so tem uma lista de ingredientes
    if(len(h2List) < 2):
        ingredientsList = ingredientDiv.find_all("li")
        for ingredient in ingredientsList:
            list.append(ingredient.text.replace("\n", ""))
        obj.hasIParts = False
        
    #Tem varias listas de ingredientes
    else:
        ulList = ingredientDiv.find_all("ul")
        index = 0
        for ul in ulList:
            lists = []
            index+=1
            ingredientsList = ul.find_all("li")
            for ingredient in ingredientsList:
                lists.append(ingredient.text.replace("\n", ""))
            list.append(lists)
        obj.hasIParts = True    
    obj.ingredients = list

    if(obj.hasIParts):
        obj.nameIParts = clean_h2_texts(h2List)

def getSteps(soup, obj):
    stepsContainer = soup.find(class_='preparo mt-4 mb-4')

    h2List = stepsContainer.find_all('h2')
    list = []

     #so tem uma lista de passos
    if(len(h2List) < 2):
        stepsContainer = soup.find("ol")
        class_ = stepsContainer['class']
        steps = []
        if(class_[0] == 'lista-preparo-1'):
            steps = stepsContainer.find_all("span")       
        if(class_[0] == 'noimg'):
            steps = stepsContainer.find_all("li")
        i = 1
        for step in steps:
            list.append(step.text.replace("\n", "")) 
            i+=1
        obj.hasSParts = False
    #Tem varias listas de passos        
    else:
        stepsContainer = soup.find_all("ol")
        index = 0
        class_ = stepsContainer[0]['class']
        
        for stepsList in stepsContainer:   
            lists = []         
            index += 1           
            steps = []
            if(class_[0] == 'lista-preparo-1'):
                steps = stepsList.find_all("span")       
            if(class_[0] == 'noimg'):
                steps = stepsList.find_all("li")
            i = 1
            for step in steps:
                lists.append(step.text.replace("\n", "")) 
                i+=1
            if(len(lists) != 0):
                list.append(lists)
        if(len(list) == 1):
            list = list[0]        
            obj.hasSParts = False
        else:
            obj.hasSParts = True  
    obj.steps = list
    if(obj.hasSParts):
        obj.nameSParts = clean_h2_texts(h2List)
    
def print_recipe(rec):
    print(f"Titulo: {rec.title}")
    print(f"Porções: {rec.portion}")
    print(f"Tempo: {rec.time}")
    print(f"Tem Ingredientes Partes: {rec.hasIParts}")
    print(f"Tem Passos Partes: {rec.hasSParts}")
    
    if(rec.hasIParts):
        print(f"=== Ingredientes:")
        index = 0
        for list in rec.ingredients:
            print(f"============= {rec.nameIParts[index]}")
            index += 1
            i = 1
            for item in list:
                print(str(i)+ ": "+item)
                i+=1        
    else:
        print("=== Ingredientes:\n")
        i = 1
        for item in rec.ingredients:
           print(str(i)+ ": "+item)
           i+=1 

    if(rec.hasSParts):
        print("=== Passos:\n")
        index = 0
        for list in rec.steps:
            print(f"============= {rec.nameSParts[index]}")
            i = 1
            index +=1
            for item in list:
                print(str(i)+ ": "+item)
                i+=1
    else:
        print("=== Passos:\n")
        i = 1
        for item in rec.steps:
           print(str(i)+ ": "+item)
           i+=1

def clean_h2_texts(h2List):
    cleaned_list = []
    for item in h2List:
        cleaned_text = item.text.replace("\n", "")
        cleaned_list.append(cleaned_text)
    return cleaned_list