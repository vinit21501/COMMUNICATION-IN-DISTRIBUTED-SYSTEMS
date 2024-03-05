import grpc
import market_pb2
import market_pb2_grpc
import uuid
from concurrent import futures
import threading

class User():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.uuid = str(uuid.uuid1())
    def getip(self):
        return self.ip + ':' + self.port
    def getuuid(self):
        return self.uuid
    def setport(self, port):
        self.port = port
    def getport(self):
        return self.port

class NotificationServicer(market_pb2_grpc.NotificationServicer):
    def Notify(self, request, context):
        # print(request)
        item = request
        print()
        print('#' * 50)
        print(f'The Following Item has been updated:')
        print("Item ID:\t",item.itemId)
        print("Price:\t\t",item.price)
        print("Name:\t\t",item.name)
        print("Category:\t",item.category)
        print("Discription:\t",item.description)
        print("Quantity:\t",item.quantity)
        print("Rating:\t\t",item.rating)
        print("Seller:\t\t",item.sellerAddress)
        print('#' * 50)
        print('Option number: ')
        reply = market_pb2.SuccessReply()
        reply.success = True
        return reply

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    market_pb2_grpc.add_NotificationServicer_to_server(NotificationServicer(), server)
    server.add_insecure_port("[::]:" + '50052')
    server.start()
    server.wait_for_termination()

def run():
    sellerDetails = User('localhost', '50052')
    with grpc.insecure_channel('localhost:50051') as channel:
    # sellerDetails = User('34.0.3.104', '50052')
    # with grpc.insecure_channel('34.0.4.70:50051') as channel:
        stub = market_pb2_grpc.SellerStub(channel)
        while(True):
            print("1. RegisterSeller")
            print("2. SellItem")
            print("3. UpdateItem")
            print("4. DeleteItem")
            print("5. DisplaySellerItems")
            print("6. Close")
            try:
                option=input("Option numer: ")
                if(option=="1"):
                    # inSellPort=input("Seller Port: ")
                    # sellerDetails.setport(inSellPort)
                    request=market_pb2.SellerRegisterRequest()
                    request.sellerAddress=sellerDetails.getip()
                    request.uuid=sellerDetails.getuuid()
                    reply=stub.RegisterSeller(request)
                    # serve(sellerDetails)
                    # liveServer = threading.Thread(target=serve, daemon=True)
                    # liveServer.start()
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
                    # inSellAdd=input("Seller Address: ")
                    request=market_pb2.SellerItemsRequest()
                    request.name=inName
                    request.price=inPrice
                    request.category=inCat
                    request.description=inDes
                    request.quantity=inQuantity
                    request.sellerAddress=sellerDetails.getip()
                    request.uuid=sellerDetails.getuuid()
                    reply=stub.SellItem(request)
                    if(reply.success):
                        print("SUCCESS")
                    else:
                        print("FAIL")
                elif(option=="3"):
                    inID=int(input("ItemID: "))
                    inPrice=input("New Price: ")
                    inQuantity=input("New Quantity: ")
                    # inSellAdd=input("Seller Address: ")
                    request=market_pb2.UpdateItemsDetailsRequest()
                    request.itemId=inID
                    request.price=inPrice
                    request.quantity=inQuantity
                    request.sellerAddress=sellerDetails.getip()
                    request.uuid=sellerDetails.getuuid()
                    reply=stub.UpdateItem(request)
                    if(reply.success):
                        print("SUCCESS")
                    else:
                        print("FAIL")
                elif(option=="4"):
                    inID=int(input("ItemID: "))
                    # inSellAdd=input("Seller Address: ")
                    request=market_pb2.DeleteItemRequest()
                    request.itemId=inID
                    request.sellerAddress=sellerDetails.getip()
                    request.uuid=sellerDetails.getuuid()
                    reply=stub.DeleteItem(request)
                    if(reply.success):
                        print("SUCCESS")
                
                    else:
                        print("FAIL")
                elif(option=="5"):
                    # inSellAdd=input("Seller Address: ")
                    request=market_pb2.SellerRegisterRequest()
                    request.sellerAddress=sellerDetails.getip()
                    request.uuid=sellerDetails.getuuid()
                    reply=stub.DisplaySellerItems(request)
                    print("#"*50)
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
                    print("#"*50)
                # elif option == '6':
                #     # inSellAdd=input("Seller Address: ")
                #     request=market_pb2.SellerRegisterRequest(sellerAddress=inSellAdd)
                #     reply = stub.NotifyClient(request)
                #     print("#"*50)
                #     for item in reply:
                #         print("Item ID:\t",item.itemId)
                #         print("Price:\t\t",item.price)
                #         print("Name:\t\t",item.name)
                #         print("Category:\t",item.category)
                #         print("Discription:\t",item.description)
                #         print("Quantity:\t",item.quantity)
                #         print("Rating:\t\t",item.rating)
                #         print("Seller:\t\t",item.sellerAddress)
                #         print("-"*50)
                #     print("#"*50)
                elif option=="6":
                    break
                else:
                    print("Invalid Commands")
            except:
                print('Invalid Argument')

if __name__ == "__main__":
    try:
        # run()

        seller = threading.Thread(target=run, daemon=True)
        seller.start()
        liveServer = threading.Thread(target=serve, daemon=True)
        liveServer.start()
        liveServer.join()
        seller.join()
    except:
        print('Interrupt!')