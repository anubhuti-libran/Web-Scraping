from bs4 import BeautifulSoup
import requests 
import pandas as pd


url = "https://www.programmableweb.com/apis/directory"
N_APIs={}
API_NO = 0

while True:

    response = requests.get(url)
    #print(response)

    data = response.text
    #print(data)

    soup = BeautifulSoup(data,'html.parser')
    #print(soup)

    interfaces = soup.find_all('tr',{'class':['even','odd']})
    
    for interface in interfaces:
        title = interface.find('td',{"class":"views-field views-field-title col-md-3"}).text
        #print(title)    
        categ = interface.find('td',{"class":"views-field views-field-field-article-primary-category"})
        #to remove the error of attribute erro : 'none type' object
        #print(categ)
        category= categ.text if categ else "N/A"
        #print(categ)
        descrip = interface.find('td',{"class":"views-field views-field-search-api-excerpt views-field-field-api-description hidden-xs visible-md visible-sm col-md-8"}).text
        #print(descrip)
        
        link_tag = interface.find('a')
        if link_tag.get('href'):
           link = "https://www.programmableweb.com" + link_tag.get('href') 
    
           #print("TITLE: ", title,"\nCATEGORY: ", categ, "\nDESCRIPTION: ", descrip, "\nLINK: ", link,"\n--------")
           #FOR ABSOLUTE DESCRIPTION OF THE TITLES
           d_response = requests.get(link)
           d_data = d_response.text
           d_soup = BeautifulSoup(d_data,'html.parser')
           ab_desc = d_soup.find('div',{'class':'api_description tabs-header_description'})
           description = ab_desc.text if ab_desc else "N/A"
           #print(description)
            
           API_NO+= 1
           N_APIs[API_NO] = [title, descrip, category, link]
           
           print("TITLE: ", title,"\nCATEGORY: ", category, "\nDESCRIPTION: ", descrip, "\nLINK: ", link,"\nDETAILED DESCRIPTION: ", description,"\n--------")
   
    
    #for the next page the url will be different
    url_tag = soup.find('a',{'title':'Go to next page'})
    #condition for the the last page where we have an empty 'a' tag
    if url_tag.get('href'):
        #here we get an absolute url
         url = 'https://www.programmableweb.com' + url_tag.get('href')
         print(url)
    else:
         break
    
    print('TOTAL NUMBER OF API: ',API_NO)
    API_df = pd.DataFrame.from_dict(N_APIs, orient = 'index', columns = ['title','descrip','category', 'link'])
    API_df.head()
    API_df.to_csv('C:/Users/Anubhuti Singh/.spyder-py3/api.csv')
    