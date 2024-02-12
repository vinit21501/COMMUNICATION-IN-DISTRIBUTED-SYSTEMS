import grpc
import market_pb2
import market_pb2_grpc
import uuid

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        sellerUuid = str(uuid.uuid1())
        while(True):
            stub = market_pb2_grpc.SellerStub(channel)
            print("1. RegisterSeller")
            print("2. SellItem")
            print("3. UpdateItem")
            print("4. DeleteItem")
            print("5. DisplaySellerItems")
            print("6. NotifyClient")
            print("7. Close")
            # try:
            option=input("Option numer: ")
            if(option=="1"):
                inSellAdd=input("Seller Address: ")
                request=market_pb2.SellerRegisterRequest()
                request.sellerAddress=inSellAdd
                request.uuid=sellerUuid
                reply=stub.RegisterSeller(request)
                if(reply.success):
                    print("SUCCESS")
                else:
                    print("FAIL")
            elif(option=="2"):
                inName=input("Name: ")
                inPrice=float(input("Price: "))
                inCat=input("Category: ")
                inDes=input("Description: ")
                inQuantity=int(input("Quantity: "))
                inSellAdd=input("Seller Address: ")
                request=market_pb2.SellerItemsRequest()
                request.name=inName
                request.price=inPrice
                request.category=inCat
                request.description=inDes
                request.quantity=inQuantity
                request.sellerAddress=inSellAdd
                request.uuid=sellerUuid
                reply=stub.SellItem(request)
                if(reply.success):
                    print("SUCCESS")
                else:
                    print("FAIL")
            elif(option=="3"):
                inID=int(input("ItemID: "))
                inPrice=input("New Price: ")
                inQuantity=input("New Quantity: ")
                inSellAdd=input("Seller Address: ")
                request=market_pb2.UpdateItemsDetailsRequest()
                request.itemId=inID
                request.price=inPrice
                request.quantity=inQuantity
                request.sellerAddress=inSellAdd
                request.uuid=sellerUuid
                reply=stub.UpdateItem(request)
                if(reply.success):
                    print("SUCCESS")
                else:
                    print("FAIL")
            elif(option=="4"):
                inID=int(input("ItemID: "))
                inSellAdd=input("Seller Address: ")
                request=market_pb2.DeleteItemRequest()
                request.itemId=inID
                request.sellerAddress=inSellAdd
                request.uuid=sellerUuid
                reply=stub.DeleteItem(request)
                if(reply.success):
                    print("SUCCESS")
            
                else:
                    print("FAIL")
            elif(option=="5"):
                inSellAdd=input("Seller Address: ")
                request=market_pb2.SellerRegisterRequest()
                request.sellerAddress=inSellAdd
                request.uuid=sellerUuid
                reply=stub.DisplaySellerItems(request)
                print("-"*50)
                for item in reply:
                    print("Item ID:\t",item.itemId)
                    print("Price:\t\t",item.price)
                    print("Name:\t\t",item.name)
                    print("Category:\t",item.category)
                    print("Discription:\t",item.description)
                    print("Quantity:\t",item.quantity)
                    print("Rating:\t\t",item.rating)
                    print("Seller:\t\t",item.sellerAddress)
                    print("-"*50)
            elif option == '6':
                inSellAdd=input("Seller Address: ")
                request=market_pb2.SellerRegisterRequest(sellerAddress=inSellAdd)
                reply = stub.NotifyClient(request)
                print("-"*50)
                for item in reply:
                    print("Item ID:\t",item.itemId)
                    print("Price:\t\t",item.price)
                    print("Name:\t\t",item.name)
                    print("Category:\t",item.category)
                    print("Discription:\t",item.description)
                    print("Quantity:\t",item.quantity)
                    print("Rating:\t\t",item.rating)
                    print("Seller:\t\t",item.sellerAddress)
                    print("-"*50)
            # except:
            #     print('Invalid Argument')
            if option=="7":
                break
            elif 1 > int(option) > 7:
                print("Invalid Commands")

if __name__ == "__main__":
    run()
