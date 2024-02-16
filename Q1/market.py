import grpc
import market_pb2
import market_pb2_grpc
from concurrent import futures

products = []
buyerNotification = {}
sellerNotification = {}
sellerRegistered = []
wishList = {}
rating = {}
productUniqueId = 0

def sendNotification(product, serverIP):
    with grpc.insecure_channel(serverIP) as channel:
        stub = market_pb2_grpc.NotificationStub(channel)
        # req = market_pb2.test()
        # req.check = 'running'
        rep = stub.Notify(product)
        print(f'Notification sent : {rep.success}')

class BuyerServicer(market_pb2_grpc.BuyerServicer):
    # option 1
    def SearchItem(self, request, context):
        cat = request.category
        itmName = request.itemName
        print(f'Search request for Item name: "{itmName}", Category: "{cat}".')
        if itmName == '':
            if cat == 'ANY' or cat == 'any' or cat == '':
                for product in products:
                    yield product
            else:
                for product in products:
                    if product.category == cat:
                        yield product
        elif cat == 'ANY' or cat == 'any' or cat == '':
            for product in products:
                if product.itemName == itmName:
                    yield product
        else:
            for product in products:
                if product.itemName == itmName and product.category == cat:
                    yield product

    def BuyItem(self, request, context):
        # option 2
        reply = market_pb2.SuccessReply()
        product = findProduct(request.itemId)
        print(f'Buy request {request.quantity} of item {request.itemId}, from {request.buyerUuid}')
        if product:
            if product.quantity - request.quantity >= 0:
                # if product.sellerAddress in sellerNotification:
                #     sellerNotification[product.sellerAddress].add(product.itemId)
                # else:
                #     sellerNotification[product.sellerAddress] = set([product.itemId])
                reply.success = True
                product.quantity -= request.quantity
                print(product.sellerAddress)
                sendNotification(product, product.sellerAddress)
                return reply
        reply.success = False
        return reply

    def AddToWishList(self, request, context):
        # option 3
        reply = market_pb2.SuccessReply()
        product = findProduct(request.itemId)
        if product:
            reply.success = True
            if request.buyerAddress in wishList:
                wishList[request.buyerAddress].add(request.itemId)
            else:
                wishList[request.buyerAddress] = set([request.itemId])
        else:
            reply.success = False
        print(f'WishList request item {request.itemId}, from {request.buyerUuid}')
        return reply

    def RateItem(self, request, context):
        # option 4
        reply = market_pb2.SuccessReply()
        print(f'{request.buyerUuid} rated item {request.itemId} with {request.rating} stars.')
        if request.buyerUuid in rating:
            for rate in rating[request.buyerUuid]:
                if request.itemId == rate[0]:
                    reply.success = False
                    return reply
        else:
            rating[request.buyerUuid] = set()
        product = findProduct(request.itemId)
        if product:

            if request.rating.is_integer() and 1 <= int(request.rating) <= 5:
                rate = int(request.rating)
                rating[request.buyerUuid].add((product.itemId, rate))
                product.rating = product.rating * product.totalRating + rate
                product.totalRating += 1
                product.rating /= product.totalRating
                reply.success = True
                return reply
        reply.success = False
        return reply

    def NotifyClient(self, request, context):
        if request.buyerUuid in buyerNotification:
            temp = buyerNotification[request.buyerUuid]
            buyerNotification[request.buyerUuid] = set()
            for productID in temp:
                product = findProduct(productID)
                if product:
                    yield product

def credentialsCheck(request):
    for seller in sellerRegistered:
        if seller.sellerAddress == request.sellerAddress and seller.uuid == request.uuid:
            return True
    return False

def findProduct(itemId):
    for product in products:
        if product.itemId == itemId:
            return product
    return

class SellerServicer(market_pb2_grpc.SellerServicer):
    def RegisterSeller(self, request, context):
        reply = market_pb2.SuccessReply()
        sellerAdds = request.sellerAddress
        uuid = request.uuid
        if credentialsCheck(request):
            reply.success = False
            print(f'Seller already joined with {sellerAdds}, uuid = {uuid}')
            return reply
        sellerRegistered.append(request)
        reply.success = True
        print(f'Seller join request from {sellerAdds}, uuid = {uuid}')
        return reply

    def SellItem(self, request, context):
        reply = market_pb2.SuccessReply()
        if credentialsCheck(request):
            reply.success = True
            product = market_pb2.ItemDetailsReply()
            global productUniqueId
            product.itemId = productUniqueId
            productUniqueId += 1
            product.price = request.price
            product.name = request.name
            product.category = request.category
            product.description = request.description
            product.quantity = request.quantity
            product.totalRating = 0
            product.rating = 0
            product.sellerAddress = request.sellerAddress
            products.append(product)
            print(f'Sell Item request from {request.sellerAddress}')
            return reply
        reply.success = False
        print(f'Invalid seller credentials {request.sellerAddress}, uuid = {request.uuid}')
        return reply

    def UpdateItem(self, request, context):
        reply = market_pb2.SuccessReply()
        if credentialsCheck(request):
            product = findProduct(request.itemId)
            if product and product.sellerAddress == request.sellerAddress:
                reply.success = True
                try:
                    if request.price != '':
                        product.price = float(request.price)
                    if request.quantity != '':
                        product.quantity = int(request.quantity)
                    print(f'Update Item {request.itemId} request from {request.sellerAddress}')
                    for buyer in wishList:
                        for productId in wishList[buyer]:
                            if productId == request.itemId:
                                # if buyer in buyerNotification:
                                #     buyerNotification[buyer].add(productId)
                                # else:
                                #     buyerNotification[buyer] = set([productId])
                                print(buyer)
                                sendNotification(product, buyer)
                    return reply
                except:
                    reply.success = False
                    print(f'Product is not update with Item Id {request.itemId}')
                    return reply
            else:
                reply.success = False
                print(f'Product not found with Item Id {request.itemId}')
                return reply
        reply.success = False
        print(f'Invalid seller credentials {request.sellerAddress}, uuid = {request.uuid}')
        return reply

    def DeleteItem(self, request, context):
        reply = market_pb2.SuccessReply()
        if credentialsCheck(request):
            product = findProduct(request.itemId)
            if product and product.sellerAddress == request.sellerAddress:
                reply.success = True
                products.remove(product)
                print(f'Delete Item {request.itemId} request from {request.sellerAddress}')
                return reply
            else:
                reply.success = False
                print(f'product not found with Item Id {request.itemId}')
                return reply
        reply.success = False
        print(f'Invalid seller credentials {request.sellerAddress}, uuid = {request.uuid}')
        return reply
                

    def DisplaySellerItems(self, request, context):
        print(f'Display Item request from {request.sellerAddress}')
        if credentialsCheck(request):
            for product in products:
                if product.sellerAddress == request.sellerAddress:
                    yield product

    def NotifyClient(self, request, context):
        if request.sellerAddress in sellerNotification:
            temp = sellerNotification[request.sellerAddress]
            sellerNotification[request.sellerAddress] = set()
            for productID in temp:
                product = findProduct(productID)
                if product and product.sellerAddress == request.sellerAddress:
                    yield product

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    market_pb2_grpc.add_BuyerServicer_to_server(BuyerServicer(), server)
    market_pb2_grpc.add_SellerServicer_to_server(SellerServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    try:
        serve()
    except:
        print('Interrupt')