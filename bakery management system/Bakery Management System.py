
"""
BAKERY MANAGEMENT SYSTEM
IP PRACTICAL DESIGN NY HIDA ISMAIL XII-A2
WELCOME TO CHERRY DREAM BAKERY MANAGEMENT SYSTEM
MAIN MENU 
1.	CUSTOMER AND ORDER DETAILS
2.	PRODUCT DETAILS
3.	STOCK DETAILS
4.  PLACE AN ORDER
5.	SALES REPORT
6.  BACK TO HOME
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import date 
pd.set_option("display.max_rows",500)
pd.set_option("display.max_columns",500)
pd.set_option("display.width",1000)


print("------------------------------------------")
print("------------------------------------------")
print("WELCOME TO BAKERY MANAGEMENT SYSTEM")
print("------------------------------------------")
print("------------------------------------------") 

def placeanorder():

    
    def viewcart():
        df_cart=pd.read_csv("cart.csv",index_col=0)
        cart_amount=df_cart["FINAL PRICE"].sum()
        print(df_cart)
        print("\n TOTAL CART VALUE:",cart_amount)
        order(df_cart)
                
    def order(df_cart):
        print("\n")
        print("1.CONFIRM ORDER")
        print("2.BACK TO CART TO ADD MORE ITEMS")
        print("3.EXIT TO MAIN MENU")
        print()
        ch=int(input("ENTER YOUR CHOICE: "))
        if (ch==1):
            order_date=date.today()
            items=df_cart["QUANTITY"].sum()
            SUM=0
            for i in range(1,len(df_cart)+1):
                SUM=SUM+df_cart["FINAL PRICE"][i]
            gst=12.5/100*SUM #GST 12.5%
            discount=0.10*SUM # FIXED DISCOUNT 10%
            net_bill=SUM+gst-discount
            c_id=input("ENTER CUSTOMER ID:") 
            em=input("ENTER EMAIL ID:")
            n=input("ENTER NAME:")
            pn=input("ENTER PHONE NUMBER:")
            if (os.path.isfile("orders.csv")):
                df1=pd.read_csv("orders.csv",index_col=0)
                order_id=df1.iloc[len(df1)-1,0]+1
                dic={"ORDER_ID":order_id,"DATE":order_date,"CUSTOMER_ID":c_id,"NO. OF ITEMS":items,
                 "TOTAL AMOUNT":SUM,"NET BILL AMOUNT":net_bill}
                df=pd.DataFrame(dic,index=[len(df1)+1])
                df.to_csv("orders.csv",mode="a",header=None)
            else:
                order_id=101
                dic={"ORDER_ID":order_id,"DATE":order_date,"CUSTOMER_ID":c_id,"NO. OF ITEMS":items,
                 "TOTAL AMOUNT":SUM,"NET BILL AMOUNT":net_bill}
                df=pd.DataFrame(dic,index=[1])
                df.to_csv("orders.csv")
            print("ORDER CONFIRMED ")
            
            print("*"*70)
            print(" "*30,"BILLING INVOICE"," "*30)
            print("*"*70)
            print("NAME: ",n,"\t EMAIL ID: ",em)
            print("PHONE NUMBER: ",pn)
            print("DATE: ",order_date)
            bi=pd.read_csv("cart.csv",index_col=0)
            print()
            print("-"*29,"your Items","-"*29)
            print(bi)
            print()
            print("Total Amount to pay with gst and discount:",net_bill)
            print("*"*70)
            print()
            
            
            #FOR SALES REPORT
            if (os.path.isfile("sales_report.csv")):
                df=pd.read_csv("sales_report.csv",index_col=0)
                df_cart=pd.read_csv("cart.csv",index_col=0)
                df1=df_cart.drop(["QUANTITY","PRICE","FINAL PRICE"],axis=1)
                
                for i in range(1,len(df1)+1):
                    for j in range(1,len(df)+1):
                        if df["P_ID"][j]==df1["P_ID"][i]:
                            df.loc[j,"SALES"]+=1
                            break;
                    else:
                        df.loc[len(df)+1]=[df1["P_ID"][i],df1["NAME OF PRODUCT"][i],df1["CATEGORY"][i],1]
                print(df)  
                df.to_csv("sales_report.csv")
                                
            else:
                df_cart=pd.read_csv("cart.csv",index_col=0)
                p_id=df_cart["P_ID"]
                p_n=df_cart["NAME OF PRODUCT"]
                cat=df_cart["CATEGORY"]
                sale=1
                dic={"P_ID":p_id,"NAME OF PRODUCT":p_n,"CATEGORY":cat,"SALES":sale}
                s_r=pd.DataFrame(dic,index=[1])
                s_r.to_csv("sales_report.csv")
           
            
            
            os.remove("cart.csv")
            
            
        elif (ch==2):
            cart()  
        elif (ch==3):
            os.remove  ("cart.csv")
            return
        
    
    def cart( ):
        df_p=pd.read_csv("productdetails.csv",index_col=0)
        print(df_p[["PRODUCT ID","NAME OF PRODUCT","PRICE (FOR EACH)","CATEGORY/PRODUCT TYPE"]])
        print("\n")
        print("1. ADD TO CART ")
        print("2. VIEW ORDERS DETAILS")
        print("3. BACK TO MAIN MENU")
        Opt=int(input("ENTER YOUR CHOICE: "))      
        if (Opt==1):
            p_id=input("ENTER PRODUCT ID: ")
            for i in range(1,len(df_p)+1):
                if (df_p["PRODUCT ID"][i]==p_id):
                    q=int(input("ENTER QUANTITY:"))
                    name=df_p["NAME OF PRODUCT"][i]
                    price=df_p["PRICE (FOR EACH)"][i]
                    cat=df_p["CATEGORY/PRODUCT TYPE"][i]
                    ta=q*price
                    dic={"P_ID":p_id,"NAME OF PRODUCT":name,"QUANTITY":q,"PRICE":price,"CATEGORY":cat,"FINAL PRICE":ta}
                    if (os.path.isfile("cart.csv")):
                        df=pd.read_csv("cart.csv",index_col=False)
                        cart=pd.DataFrame(dic,index=[len(df)+1])
                        cart.to_csv("cart.csv",mode="a",header=None)
                    else:
                        cart=pd.DataFrame(dic,index=[1])
                        cart.to_csv("cart.csv")
                    print("YOUR ITEM ADDED TO CART SUCCESSFULLY")
                    viewcart()
                    break
            else:
                print("INVALID PRODUCT ID")
        elif (Opt==2):
            print("------VIEW ORDERS DETAILS-----------")
            print("1. VIEW ALL ORDERS")
            print("2. VIEW ORDERS OF A PARTICULAR CUSTOMER")
            c=int(input("ENTER YOUR CHOICE: "))
            if c==1:
                if (os.path.isfile("orders.csv")):
                    df=pd.read_csv("orders.csv",index_col=0)
                    print(df)
                else:
                    print("FILE DOESN'T EXIST")
            elif c==2:
                if (os.path.isfile("orders.csv")):
                    df=pd.read_csv("orders.csv",index_col=0)
                    cid=input("ENTER CUSTOMER ID: ")
                    for i in range(1,len(df)+1):
                        if df["CUSTOMER_ID"][i]==(cid):
                            print(df[df["CUSTOMER_ID"]==(cid)])
                            break
                    else:
                        print("CUSTOMER ID DOESN'T EXIST")
                else:
                    print("FILE DOESN'T EXIST")
            else:
                print("INVALID CHOICE ENTERED")
        elif (Opt==3):
            return
        
    cart()
        
    
#---------------------------------------------------------------------------------------------------------------
    


def mainmenu():
    while(True):
        print("\n")
        print("MAIN MENU :")
        print("1. CUSTOMER DETAILS")
        print("2. PRODUCT DETAILS")
        print("3. STOCK DETAILS")
        print("4. PLACE AN ORDER")
        print("5. SALES REPORT")
        print("6. BACK TO HOME")
        choice=int(input("ENTER YOUR CHOICE:"))
        if (choice==1):
            print("------------------------------------------")
            print("CUSTOMER DETAILS:")
            print("------------------------------------------")
            print(" 1. TO INSERT NEW CUSTOMER DETAILS")
            print(" 2. TO VIEW ALL CUSTOMER DETAILS ")
            print(" 3. TO SEARCH DETAILS ")
            print(" 4. TO UPDATE DETAILS ")
            print(" 5. TO DELETE DETAILS")
            option=int(input("PLEASE SELECT FROM THE ABOVE OPTION: "))
            if (option==1):
                print("------ADD CUSTOMER RECORD-----------")
                print(" ENTER FOLLOWING DETAILS: ")
                Id=input("Customer ID: ")
                name=input("Name: ")
                dob=input("Date of Birth: ")
                gender=input("Gender (M/F): ")
                phone_no=input("Phone Number: ")
                address=input("Address: ")  
                dte=date.today()
                delivery=input("Order by Delivery (Y/N): ")
                if (delivery=="Y" or delivery=="y"):
                    time_to=input("Time to be Delivered: ")
                    venue=input("Venue: ")
                else:
                    time_to="NaN"
                    venue="NAN"
                customer_details={"CUSTOMER ID":Id,"NAME":name,"DATE OF BIRTH":dob,
                                   "GENDER":gender,"PHONE NUMBER":phone_no,
                                   "ADDRESS":address,"DATE OF REGISTERATION":dte,
                                   "DELIVERY":delivery,"TIME TO BE DELIVERED":time_to,
                                   "VENUE":venue}
                if (os.path.isfile("customer_details.csv")):
                    df1=pd.read_csv("customer_details.csv",index_col=False)
                    df=pd.DataFrame(customer_details,index=[len(df1)+1])
                    df.to_csv("customer_details.csv",mode="a",header=None)
                else:
                    df=pd.DataFrame(customer_details,index=[1])
                    df.to_csv("customer_details.csv")
                print("RECORD SAVED SUCCESSFULLY")
                
            elif (option==2):
                print("CUSTOMER DETAILS")
                print("------VIEW CUSTOMER RECORD-----------")
                if (os.path.isfile("customer_details.csv")):
                    df=pd.read_csv("customer_details.csv",index_col=0)
                    pd.set_option("display.max_colwidth",None)
                    print(df)
                else:
                    print("FILE DOESN'T EXIST")
                
                
            elif (option==3):
                print("CUSTOMER DETAILS")
                print("------SEARCH CUSTOMER RECORD-----------")
                df=pd.read_csv("customer_details.csv",index_col=0)
                
                print("1. CUSTOMER ID ")
                print("2. CUSTOMER NAME")
                search=int(input("Choice the field on the basis of which you want to search:"))
                if (search==1):
                    c_id=input("Enter Customer ID: ")
                    print(df[df["CUSTOMER ID"]==eval(c_id)])
                elif (search==2):
                    c_name=input("Enter Customer Name: ")
                    print(df[df["NAME"]==c_name])
                else:
                    print("INVALID CHOICE ENTERED")
                
                
            elif (option==4):
                print("CUSTOMER DETAILS")
                print("------UPDATE CUSTOMER RECORD-----------")
                df=pd.read_csv("customer_details.csv",index_col=0)
                print(df[["CUSTOMER ID","NAME"]])
                c_id=input("Enter Customer ID:  ")
                for i in range(1,len(df)+1):
                    if(df["CUSTOMER ID"][i]==eval(c_id)):
                        print("YOUR RECORD HAS BEEN FOUND AND RECORD IS............")
                        print(df[df["CUSTOMER ID"]==eval(c_id)])
                        ind=df[df["CUSTOMER ID"]==eval(c_id)].index
                        print("PRESS N TO MAKE UPDATION IN NAME OR - TO RETAIN SAME NAME: ")
                        ch=input()
                        if(ch=="N" or ch=="n"):
                            c_name=input("ENTER NEW NAME: ")
                            df.loc[ind,"NAME"]=c_name
                            input("Press any key to move further")
                        print("PRESS D TO MAKE UPDATION IN DATE OF BIRTH OR - TO RETAIN SAME VALUE: ")
                        ch=input()
                        if(ch=="D" or ch=="d"):
                            c_dob=input("ENTER NEW DATE OF BIRTH: ")
                            df.loc[ind,"DATE OF BIRTH"]=c_dob
                            input("Press any key to move further")
                        print("PRESS G TO MAKE UPDATION IN GENDER OR - TO RETAIN SAME VALUE: ")
                        ch=input()
                        if(ch=="G" or ch=="g"):
                            c_gender=input("ENTER GENDER: ")
                            df.loc[ind,"GENDER"]=c_gender   
                            input("Press any key to move further")
                        print("PRESS P TO MAKE UPDATION IN PHONE NUMBER OR - TO RETAIN SAME VALUE: ")
                        ch=input( )
                        if(ch=="P" or ch=="p"):
                            c_pn=input("ENTER NEW PHONE NUMBER: ")
                            df.loc[ind,"PHONE NUMBER"]=c_pn
                            input("Press any key to move further")
                        print("PRESS A TO MAKE UPDATION IN ADDRESS OR - TO RETAIN SAME VALUE: ")
                        ch=input()   
                        if(ch=="A" or ch=="a"):
                            c_add=input("ENTER NEW ADDRESS: ")
                            df.loc[ind,"ADDRESS"]=c_add
                            input("Press any key to move further")
                        print("PRESS R TO MAKE UPDATION IN DATE OF REGISTERATION OR - TO RETAIN SAME VALUE: ")
                        ch=input() 
                        if(ch=="R" or ch=="r"):
                            c_dr=input("ENTER NEW DATE OF REGISTERATION: ")
                            df.loc[ind,"DATE OF REGISTERATION"]=c_dr
                            input("Press any key to move further")
                        print("PRESS Y TO MAKE UPDATION IN DELIVERY(Y/N) OR - TO RETAIN SAME VALUE: ")
                        ch=input() 
                        if(ch=="Y" or ch=="y"):
                            c_del=input("ENTER DELIVERY (Y/N): ")
                            df.loc[ind,"DELIVERY"]=c_del
                            if (c_del=="Y" or c_del=="y"):
                                c_time=input("ENTER TIME TO BE DELIVERED: ")
                                df.loc[ind,"TIME TO BE DELIVERED"]=c_time
                                c_venue=input("Venue: ")
                                df.loc[ind,"VENUE"]=c_venue
                                input("Press any key to move further")
                            else:
                                c_time="NaN"
                                df.loc[ind,"TIME TO BE DELIVERED"]=c_time
                                venue="NaN"
                                df.loc[ind,"VENUE"]=c_venue
                                input("Press any key to move further")
                        print("RECORD UPDATED SUCCESSFULLY")
                        break
                else:
                    print("NO RECORD FOUND OF",c_id,"ENTERED BY YOU")
                df.to_csv("customer_details.csv")
                       
    
                
                
            elif (option==5):
                print("CUSTOMER DETAILS")
                print("------DELETE CUSTOMER RECORD-----------")
                df=pd.read_csv("customer_details.csv",index_col=0)
                print(df[["CUSTOMER ID","NAME"]])
                
                print("\n")
                print("1. CUSTOMER ID ")
                print("2. CUSTOMER NAME")
                search=int(input("Choice the field on the basis of which you want to search: "))
                if (search==1):
                    c_id=input("Enter Customer ID: ")
                    print(df[df["CUSTOMER ID"]==eval(c_id)])
                    ind=df[df["CUSTOMER ID"]==eval(c_id)].index
                    
                    a=input("Are you sure you want to delete this record (Y/N): ")
                    if (a=="y" or a=="Y" or a=="Yes"):
                        df=df.drop(ind)
                        df.index=range(1,len(df)+1)
                        df.to_csv("customer_details.csv")
                        print("RECORD DELETED!")
                    else:
                        print("Record in not deleted!")
                elif (search==2):
                    c_name=input("Enter Customer Name: ")
                    print(df[df["NAME"]==(c_name)])
                    ID=input("Enter Customer ID: ")
                    ind=df[df["CUSTOMER ID"]==eval(ID)].index
                    a=input("are you sure you want to delete this record (Y/N): ")
                    if (a=="y" or a=="Y" or a=="Yes"):
                        df=(df.drop(ind))
                        df.index=range(1,len(df)+1)
                        df.to_csv("customer_details.csv")
                        print("RECORD DELETED!")
                    else:
                        print("RECORD IS NOT DELETED!")
                else:
                    print("INVALID CHOICE ENTERED")
      
                    
                
        elif (choice==2):
            print("------------------------------------------")
            print("PRODUCT DETAILS: ")
            print("------------------------------------------")
            print(" 1. TO INSERT NEW PRODUCT DETAILS ")
            print(" 2. TO VIEW ALL PRODUCT DETAILS ")
            print(" 3. TO SEARCH DETAILS ")
            print(" 4. TO UPDATE DETAILS  ")
            print(" 5. TO DELETE DETAIL ")
            opt=int(input("PLEASE SELECT FROM THE ABOVE OPTION: "))
            if (opt==1):
                print("PRODUCT DETAILS: ")
                print("------ADD PRODUCT RECORD-----------")
                print(" ENTER FOLLOWING DETAILS: ")
                Id=input("Product ID: ")
                name_product=input("Name of product: ")
                price=input("Price (for each): ")
                category=input("Category / product type: ")
                quantity=input("Quantity / how many available in stock: ")
                
                product_details={"PRODUCT ID":Id,"NAME OF PRODUCT":name_product,"PRICE (FOR EACH)":price,
                                   "CATEGORY/PRODUCT TYPE":category,"QUANTITY":quantity}
                if (os.path.isfile("productdetails.csv")):
                    df1=pd.read_csv("productdetails.csv",index_col=False)
                    df=pd.DataFrame(product_details,index=[len(df1)+1])
                    df.to_csv("productdetails.csv",mode="a",header=None)
                else:
                    df=pd.DataFrame(product_details,index=[1])
                    df.to_csv("productdetails.csv")
                
                print("RECORD SAVED SUCCESSFULLY")
                
                
            elif (opt==2):
                print("PRODUCT DETAILS: ")
                print("------VIEW PRODUCT RECORD-----------")
                if (os.path.isfile("productdetails.csv")):
                    df=pd.read_csv("productdetails.csv",index_col=0)
                    print(df)
                else:
                    print("FILE DOESN'T EXIST")
                
                
            elif (opt==3):
                print("PRODUCT DETAILS")
                print("------SEARCH PRODUCT RECORD-----------")
                df=pd.read_csv("productdetails.csv",index_col=0)
                
                print("1. PRODUCT ID ")
                print("2. PRODUCT NAME ")
                print("3. CATEGORY ")
                search=int(input("Choice the firld on the basis of which you want to search: "))
                if (search==1):
                    p_id=input("Enter product ID: ")
                    print(df[df["PRODUCT ID"]==p_id])
                elif (search==2):
                    p_name=input("Enter product Name: ")
                    print(df[df["NAME OF PRODUCT"]==p_name])
                elif (search==3):
                    p_cat=input("Enter Category: ")
                    print(df[df["CATEGORY/PRODUCT TYPE"]==p_cat])
                else:
                    print("INVALID CHOICE ENTERED")
                print(" ")
                
                
            elif (opt==4):
                print("PRODUCT DETAILS")
                print("------UPDATE PRODUCT RECORD-----------")
                df=pd.read_csv("productdetails.csv",index_col=0)
                print(df)
                p_id=input("Enter product ID to update:  ")
                for i in range(1,len(df)+1):
                    if(df["PRODUCT ID"][i]==(p_id)):
                        print("PRESS N TO MAKE UPDATION IN PRODUCT NAME OR - TO RETAIN SAME NAME ")
                        ch=input()
                        if(ch=="N" or ch=="n"):
                            p_name=input("ENTER PRODUCT NAME: ")
                            df.loc[i,"NAME OF PRODUCT"]=p_name
                            input("Press any key to move further")
                        print("PRESS P TO MAKE UPDATION IN PRICE OR - TO RETAIN SAME VALUE ")
                        ch=input()
                        if(ch=="P" or ch=="p"):
                            p_price=input("ENTER PRICE (FOR EACH): ")
                            df.loc[i,"PRICE (FOR EACH)"]=p_price
                            input("Press any key to move further")
                        print("PRESS C TO MAKE UPDATION IN CATEGORY/PRODUCT TYPE OR - TO RETAIN SAME NAME ")
                        ch=input()
                        if(ch=="C" or ch=="c"):
                            p_cat=input("ENTER CATEGORY/PRODUCT TYPE: ")
                            df.loc[i,"CATEGORY/PRODUCT TYPE"]=p_cat
                            input("Press any key to move further")
                        print("PRESS Q TO MAKE UPDATION IN QUANTITY OR - TO RETAIN SAME NAME ")
                        ch=input()
                        if(ch=="Q" or ch=="q"):
                            p_qua=input("ENTER NEW QUANTITY: ")
                            df.loc[i,"QUANTITY"]=p_qua
                            input("Press any key to move further")
                        print("RECORD AFTER MAKING CHANGES IS ")
                        print(df)
                        df.to_csv("productdetails.csv")
                        print("RECORD UPDATED SUCCESSFULLY")
                        break
                else:
                    print("NO RECORD FOUND OF",p_id,"ENTERED BY YOU")
               

            elif (opt==5):
                print("PRODUCT DETAILS")
                print("------DELETE PRODUCT RECORD-----------")
                df=pd.read_csv("productdetails.csv",index_col=0)
                print(df[["PRODUCT ID","NAME OF PRODUCT","CATEGORY/PRODUCT TYPE"]])
                
                print("\n")
                print("1.PRODUCT ID ") 
                print("2.NAME OF PRODUCT")
                print("3.CATEGORY/PRODUCT TYPE")
                
                search=int(input("Choice the field on the basis of which you want to search: "))
                if (search==1):
                    product_id=input("Enter Product Id: ")
                    print(df[df["PRODUCT ID"]==(product_id)])
                    index=df[df["PRODUCT ID"]==(product_id)].index
                    
                    a=input("are you sure you want to delete this record (Y/N): ")
                    if (a=="y" or a=="Y" or a=="Yes"):
                        df=df.drop(index)
                        df.index=range(1,len(df)+1)
                        df.to_csv("productdetails.csv")
                        print("RECORD DELETED!")
                    else:
                        print("Record in not deleted!")
                elif (search==2):
                    product_name=input("Enter Product Name: ")
                    print(df[df["NAME OF PRODUCT"]==product_name])
                    product_id=input("Enter PRODUCT ID: ")
                    index=df[df["PRODUCT ID"]==(product_id)].index
                    a=input("are you sure you want to delete this record (Y/N): ")
                    if (a=="y" or a=="Y" or a=="Yes"):
                        df=df.drop(index)
                        df.index=range(1,len(df)+1)
                        df.to_csv("productdetails.csv")
                        print("RECORD DELETED!")
                    else:
                        print("RECORD IS NOT DELETED!")
                elif (search==3):
                    product_c=input("Enter Product Category: ")
                    print(df[df["CATEGORY/PRODUCT TYPE"]==(product_c)])
                    product_id=input("Enter PRODUCT ID: ")
                    index=df[df["PRODUCT ID"]==(product_id)].index
                    
                    a=input("are you sure you want to delete this record (Y/N): ")
                    if (a=="y" or a=="Y" or a=="Yes"):
                        df=df.drop(index)
                        df.index=range(1,len(df)+1)
                        df.to_csv("productdetails.csv")
                        print("RECORD DELETED!")
                    else:
                        print("Record in not deleted!")            
                else:
                   print("INVALID CHOICE ENTERED")
     
        
     
        
        
            
        elif (choice==3):
            print("------------------------------------------")
            print("STOCK DETAILS")
            print("------------------------------------------")
            print(" 1. TO INSERT NEW STOCK PRODUCT DETAILS ")
            print(" 2. TO VIEW ALL STOCK PRODUCT DETAILS ")
            print(" 3. TO SEARCH DETAILS ")
            print(" 4. TO UPDATE DETAILS ")
            print(" 5. TO DELETE DETAILS ")
            op=int(input("PLEASE SELECT FROM THE ABOVE OPTION: "))
            if (op==1):
                print("----------ADD STOCK RECORD----------")
                print(" ENTER FOLLOWING DETAILS: ")
                stock_id=input("Stock Id: ")
                name_stock=input("Stock product name: ")
                availability=input("Availability: ")
                stock_details={"STOCK ID":stock_id,"STOCK_PRODUCT NAME":name_stock,"AVAILABILITY":availability}
                if (os.path.isfile("stockdetails.csv")):
                    df1=pd.read_csv("stockdetails.csv",index_col=False)
                    df=pd.DataFrame(stock_details,index=[len(df1)+1])
                    df.to_csv("stockdetails.csv",mode="a",header=None)
                else:
                    df=pd.DataFrame(stock_details,index=[1])
                    df.to_csv("stockdetails.csv")
                print("RECORD SAVED SUCCESSFULLY")
                
                
            elif (op==2):
                print("STOCK DETAILS: ")
                print("----------VIEW STOCK RECORD----------")
                if (os.path.isfile("stockdetails.csv")):
                    df=pd.read_csv("stockdetails.csv",index_col=0)
                    print(df)
                else:
                    print("FILE DOESN'T EXIST")
                
                
            elif (op==3):
                print("STOCK DETAILS")
                print("----------SEARCH STOCK RECORD----------")
                df=pd.read_csv("stockdetails.csv",index_col=0)
                
                print("1. STOCK ID ")
                print("2. STOCK PRODUCT NAME")
                search=int(input("Choice the firld on the basis of which you want to search: "))
                if (search==1):
                    s_id=input("Enter stock ID: ")
                    print(df[df["STOCK ID"]==eval(s_id)])
                elif (search==2):
                    s_name=input("Enter stock product Name: ")
                    print(df[df["STOCK_PRODUCT NAME"]==s_name])
                else:
                    print("INVALID CHOICE ENTERED")
                
                
            elif (op==4):
                print("STOCK DETAILS")
                print("----------UPDATE STOCK RECORD----------")
                df=pd.read_csv("stockdetails.csv",index_col=0)
                print(df)
                s_id=input("Enter Stock ID to update:  ")
                
                for i in range(1,len(df)+1):
                    if(df["STOCK ID"][i]==eval(s_id)):
                        ind=df[df["STOCK ID"]==eval(s_id)].index
                        print("PRESS N TO MAKE UPDATION IN STOCK PRODUCT NAME OR - TO RETAIN SAME NAME ")
                        ch=input()
                        if(ch=="N" or ch=="n"):
                                s_name=input("ENTER STOCK PRODUCT NAME: ")
                                df.loc[ind,"STOCK_PRODUCT NAME"]=s_name
                                input("Press any key to move further")
                        print("PRESS A TO MAKE UPDATION IN AVAILABILITY OR - TO RETAIN SAME VALUE ")
                        ch=input()
                        if(ch=="A" or ch=="a"):
                            s_ava=input("ENTER AVAILABILITY: ")
                            df.loc[ind,"AVAILABILITY"]=s_ava
                        print("RECORD AFTER MAKING CHANGE IS ")
                        print(df)
                        print("RECORD UPDATED SUCCESSFUL")
                        break
                else:
                    print("NO RECORD FOUND OF",s_id,"ENTERED BY YOU")
                df.to_csv("stockdetails.csv")
                

            elif (op==5):
                print("STOCK DETAILS")
                print("----------DELETE STOCK RECORD----------")
                df=pd.read_csv("stockdetails.csv",index_col=0)
                print(df[["STOCK ID","STOCK_PRODUCT NAME"]])
                print("\n")
                print("1.STOCK ID ")
                print("2.STOCK PRODUCT NAME")
                search=int(input("Choice the field on the basis of which you want to search: "))
                if (search==1):
                    stock_id=input("Enter stock ID: ")
                    print(df[df["STOCK ID"]==eval(stock_id)])
                    i=df[df["STOCK ID"]==eval(stock_id)].index
                    
                    a=input("are you sure you want to delete this record (Y/N): ")
                    if (a=="y" or a=="Y" or a=="Yes"):
                        df=df.drop(i)
                        df.index=range(1,len(df)+1)
                        df.to_csv("stockdetails.csv")
                        print("RECORD DELETED!")
                    else:
                        print("RECORD IS NOT DELETED!")
                elif (search==2):
                    stock_name=input("Enter Stock Product Name: ")
                    print(df[df["STOCK_PRODUCT NAME"]==stock_name])
                    stock_id=input("Enter stock ID: ")
                    i=df[df["STOCK ID"]==eval(stock_id)].index
                    a=input("are you sure you want to delete this record (Y/N): ")
                    if (a=="y" or a=="Y" or a=="Yes"):
                        df=df.drop(i)
                        df.index=range(1,len(df)+1)
                        df.to_csv("stockdetails.csv")
                        print("RECORD DELETED!")
                    else:
                        print("RECORD IS NOT DELETED!")
                else:
                    print("INVALID CHOICE ENTERED")
            
                
        
        elif (choice==4): 
            placeanorder()
  
           
        
        elif (choice==5):
            if (os.path.isfile("sales_report.csv")):
                df_sales=pd.read_csv("sales_report.csv",index_col=0)
                print("1.TO VIEW SALES OF EACH PRODUCT")
                print("2.TO VIEW SALES OF IN EACH CATEGORY")
                choice=int(input("ENTER YOUR CHOICE:"))
                if choice==1:
                    df_sales.plot(kind="bar",x="NAME OF PRODUCT",title="SALES OF EACH PRODUCT",
                                  ylabel="SALES",color="lightpink",edgecolor="k",
                                  linewidth=2,linestyle="solid",width=0.5)
                    plt.show()
                elif choice==2:
                    gdf=df_sales.groupby("CATEGORY").sum()
                    gdf.plot(kind="bar",title="CATEGORY V/S QUANTITY GRAPH",
                             ylabel="SALES",color="orange",edgecolor="black",
                             linewidth=2,linestyle="solid",width=0.5)
                    plt.show()  
                else:
                    print("INVALID CHOICE ENTERED")
            else:
                print("NO SALES RECORDED")
            
        elif (choice==6):
            break
        
        else:
           print("INVALID CHARACTER INDENTIFIED")
mainmenu()

#---------------------------------------------------------------------------------------------------------------

'''while (True):
    print(" ")
    print("1. ADMIN LOGIN ")
    print("2. NEW ADMIN REGISTERATION ")
    print("3. LOG OUT ")
    choice=int(input("ENTER YOUR CHOICE: "))
    if (choice == 1):
        user_id_=input("USER ID: ")
        password_=input("PASSWORD: ")

        if (os.path.isfile("login_detail.csv")):
            df=pd.read_csv("login_detail.csv",index_col=0)

            for i in range(0,len(df)+1):
                if df["USER ID"].iloc[i-1] == user_id_ and df["PASSWORD"].iloc[i-1] == password_:
                    print(" ")
                    print("WELCOME BACK",df["NAME"][i],"TO OUR BAKERY MANAGEMENT SYSTEM ")
                    input("Press any key to access Main Menu: ")
                    mainmenu()
                    break
            else:
                print("INVALID CREDENTIAL!!! PLEASE CHECK YOUR USER ID AND PASSWORD")
        else:
            print("YOU ARE NOT REGISTERED! PLEASE REGISTER YOURSELF")
    
    elif (choice == 2):
        user_id=input("ENTER USER ID: ")
        password=input("ENTER PASSWORD: ")
        re_password=input("CONFIRM PASSWORD: ")
        if (password==re_password):
            print("please enter the following details: ")
            name=input("Name: ")
            dob=input("Date of Birth: ")
            gender=input("Gender (M/F): ")
            phone_no=input("Phone Number: ")
            email_id=input("Email ID: ")
            dic={"USER ID":user_id,"PASSWORD":password,"NAME":name,
                 "DATE OF BIRTH":dob,"GENDER":gender,"PHONE NUMBER":phone_no,
                 "EMAIL ID":email_id}
            if (os.path.isfile("login_detail.csv")):
                df1=pd.read_csv("login_detail.csv")
                df=pd.DataFrame(dic,index=[len(df1)+1])
                df.to_csv("login_detail.csv",mode="a",header=None)
            else:
                df=pd.DataFrame(dic,index=[1])
                df.to_csv("login_detail.csv")
            print("-----------------------------------")
            print("YOU ARE SUCCESSFULLY REGISTERED ")
            print("-----------------------------------")
        else:
            print(" PASSWORD DOESN'T MATCH! please retype the password carefully")
            
    elif (choice == 3):
        
        print("-----------------------------------")
        print("THANK YOU FOR USING OUR SYSTEM")
        print("-----------------------------------")     
        break
    else:
        print("INVALID CHOICE ENTERED") 

'''
        
               
         
            
    
















