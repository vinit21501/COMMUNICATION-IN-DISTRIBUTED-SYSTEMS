import grpc
import uuid
import market_pb2
import market_pb2_grpc
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
    server.add_insecure_port("[::]:" + '50053')
    server.start()
    server.wait_for_termination()

def run():
    buyerDetail = User('localhost', '50053')
    with grpc.insecure_channel('localhost:50051') as channel:
    # buyerDetail = User('34.0.8.139', '50053')
    # with grpc.insecure_channel('34.0.3.104:50051') as channel:
        stub = market_pb2_grpc.BuyerStub(channel)
        while(True):
                print("1. SearchItem")
                print("2. BuyItem")
                print("3. AddToWishList")
                print("4. RateItem")
                print("5. Close")
                option = input("Option number: ")
                try:
                    if(option == "1"):
                        inName=input("Item name: ")
                        inCat=input("Category: ")
                        request=market_pb2.SellerItemsRequest()
                        request.name=inName
                        request.category=inCat
                        reply=stub.SearchItem(request)
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
                    elif option =="2":
                        inID=int(input("ItemID: "))
                        inQuantity=int(input("Quantity: "))
                        request=market_pb2.BuyingRequest()
                        request.itemId=inID
                        request.quantity=inQuantity
                        request.buyerAddress=buyerDetail.getip()
                        request.buyerUuid = buyerDetail.getuuid()
                        reply=stub.BuyItem(request)
                        if(reply.success):
                            print("SUCCESS")
                        else:
                            print("FAIL")
                    elif option == "3":
                        inID=int(input("ItemID: "))
                        request=market_pb2.WishListRequest()
                        request.itemId=inID
                        request.buyerAddress=buyerDetail.getip()
                        request.buyerUuid = buyerDetail.getuuid()
                        reply=stub.AddToWishList(request)
                        # serve(buyerDetail)
                        if(reply.success):
                            print("SUCCESS")
                        else:
                            print("FAIL")
                    elif option == "4":
                        inID=int(input("ItemID: "))
                        inRating=input("Rating between(1 to 5): ")
                        request=market_pb2.RatingRequest()
                        request.itemId=inID
                        request.buyerAddress=buyerDetail.getip()
                        request.buyerUuid = buyerDetail.getuuid()
                        request.rating=inRating
                        reply=stub.RateItem(request)
                        if(reply.success):
                            print("SUCCESS")
                        else:
                            print("FAIL")
                    # elif option == "5":
                    #     request=market_pb2.BuyerNotificationRequest()
                    #     request.buyerAddress=buyerDetail.getip()
                    #     request.buyerUuid = buyerDetail.getuuid()
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
                    elif option=="5":
                        break
                    else:
                        print("Invalid Commands")
                except:
                    print('Invalid Argument')

if __name__ == "__main__":
    try:
        # run()
        liveServer = threading.Thread(target=serve, daemon=True)
        buyer = threading.Thread(target=run, daemon=True)
        liveServer.start()
        buyer.start()
        liveServer.join()
        buyer.join()
    except:
        print('Interrupt!')