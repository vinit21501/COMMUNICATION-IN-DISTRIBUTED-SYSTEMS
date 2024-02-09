import grpc
import market_pb2
import market_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = market_pb2_grpc.BuyerStub(channel)
        while(True):
                print("1. SearchItem")
                print("2. BuyItem")
                print("3. AddToWishList")
                print("4. RateItem")
                print("5. NotifyClient")
                print("6. Close")
                option = input("option number: ")
                # try:
                if(option == "1"):
                    inName=input("Item name: ")
                    inCat=input("Category: ")
                    request=market_pb2.SellerItemsRequest()
                    request.name=inName
                    request.category=inCat
                    reply=stub.SearchItem(request)
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
                elif option =="2":
                    inID=int(input("ItemID: "))
                    inQuantity=int(input("Quantity: "))
                    inBuyAdd=input("Buyer Address: ")
                    request=market_pb2.BuyingRequest()
                    request.itemId=inID
                    request.quantity=inQuantity
                    request.buyerAddress=inBuyAdd
                    reply=stub.BuyItem(request)
                    if(reply.success):
                        print("SUCCESS")
                    else:
                        print("FAIL")
                elif option == "3":
                    inID=int(input("ItemID: "))
                    inBuyAdd=input("Buyer Address: ")
                    request=market_pb2.WishListRequest()
                    request.itemId=inID
                    request.buyerAddress=inBuyAdd
                    reply=stub.AddToWishList(request)
                    if(reply.success):
                        print("SUCCESS")
                    else:
                        print("FAIL")
                elif option == "4":
                    inID=int(input("ItemID: "))
                    inBuyAdd=input("Buyer Address: ")
                    inRating=int(input("Rating between(1 to 5): "))
                    request=market_pb2.RatingRequest()
                    request.itemId=inID
                    request.buyerAddress=inBuyAdd
                    request.rating=inRating
                    reply=stub.RateItem(request)
                    if(reply.success):
                        print("SUCCESS")
                    else:
                        print("FAIL")
                elif option == "5":
                    inBuyAdd=input("Buyer Address: ")
                    request=market_pb2.BuyerNotificationRequest(buyerAddress=inBuyAdd)
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
                if option=="6":
                    break
                elif 1 > int(option) > 6:
                    print("Invalid Commands")

if __name__ == "__main__":
    run()