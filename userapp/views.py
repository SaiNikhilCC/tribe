from django.shortcuts import render
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework.views import APIView
from . import user_serializer
from sadmin import admin_serializers
from tribe.customauth import CustomAuthentication
import requests
from maintribe import models
from jsonschema import ValidationError
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
import random
from rest_framework.filters import SearchFilter
from django.db.models import Q
from rest_framework.renderers import JSONRenderer

# FAST2SMS API To Send OTP Code
url = "https://www.fast2sms.com/dev/bulkV2"
def sendsms(num, phone,device_id):
    payload = f"sender_id=FTWSMS&message=To Verify Your Mobile Number with The Neon Tribe is {num} {device_id}&route=v3&numbers={phone}"
    print(payload)
    headers = {
        'authorization': "ulBGWHeNb4qJ9KmyA1fip0RdPYh6kXjwEscTSQ3ODFvC2rgnIZezvgnxpTBcjmlJZQAkY7LKVSHGMU4d",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = "sent"
    response = requests.request("POST", url, data=payload, headers=headers)
    return True
# End of FAST2SMS API

# USER REGISTRATION AND REQUESTS FOR OTP
class RegisterUser(APIView):
    try:
        def post(self, request):
            if models.Users.objects.filter(phone=request.data['phone']):
                return Response({
                    'status':400,
                    'errors':'user already exists with this number try loging in'
                })
            serializer = user_serializer.UserSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'status': 403, 'errors': serializer.errors, 'message': 'some error occurred'})
            serializer.save()
            otp = serializer.data['otp']
            phone = serializer.data['phone']
            device_id = serializer.data['device_id']
            sendsms(otp,phone,device_id)
            print("OTP to Verify Your Number is : ",
                  otp, " -----> sent to : ", phone)
            return Response({
                'status': 200,
                'data': serializer.data,
                'message': 'success'
            })
    except Exception as e:
        raise ValidationError('somthing went wrong')

# Resend OTP For User
class ResendOTP(APIView):
    def post(self,request):
        if models.Users.objects.filter(phone=request.data['phone']):
            user = models.Users.objects.get(phone=request.data['phone'])
            user.otp = random.randint(10000,99999)
            user.save()
            print(user.otp)
            sendsms(user.otp,user.phone,user.device_id)
            return Response({
                'status':200,
                'data':'OTP Sent To Your Registered Mobile Number'
            })

# USER ENTERS OTP AND GETS VERIFIED BASED ON HIS UUID AND OTP
class VerifyOtp(APIView):
    try:
        def post(self, request):
            if models.Users.objects.filter(uid=request.data["uid"], otp=request.data["otp"]):
                user = models.Users.objects.get(uid=request.data['uid'])
                user.is_verified = True
                user.otp = ""
                user.save()
                refresh = AccessToken.for_user(user)
                updated_user = models.Users.objects.filter(uid=request.data["uid"])
                serializer = user_serializer.UserSerializer(updated_user, many=True)
                response = Response({
                    'status': 200,
                    'data': serializer.data,
                    'access': str(refresh),
                    'message': 'success'
                })
                response.content_type = "application/json"
                return response
            else:
                return Response({
                    'status': 400,
                    'message': 'incorrect otp'
                })
    except Exception as e:
        raise ValidationError('something went wrong')

# Login API For End user
class Login(APIView):
    def post(self,request):
        if models.Users.objects.filter(phone=request.data['phone']):
            user = models.Users.objects.get(phone=request.data['phone'])
            user.otp = random.randint(10000,99999)
            user.save()
            sendsms(user.otp,user.phone,user.device_id)
            user_data = models.Users.objects.filter(phone=request.data['phone'])
            user_data_serializer = user_serializer.UserSerializer(user_data,many=True)
            return Response({
                'status': 200,
                'data':user_data_serializer.data,
                'message': 'OTP is Sent To Registered Phone Number'
            })
        else:
            return Response({
                'status': 400,
                'message': 'User Not Found Register Now'
            })

# User Profile
class UserProfile(APIView):
    def post(self,request):
        if models.Users.objects.filter(uid=request.data['uid']):
            user = models.Users.objects.filter(uid=request.data['uid'])
            user_data_serializer = user_serializer.UserSerializer(user,many=True)
            return Response({
                'status':200,
                'data':user_data_serializer.data,
                'message':'user profile data fetched'
            })
        else:
            return Response({
                'status':400,
                'error':'some error occurred',
                'message':'No User Found'
            })

# Edit User Profile
class EditUserProfile(APIView):
    def put(self, request,):
        try:
            obj = models.Users.objects.get(pk=request.data['uid'])
        except models.Users.DoesNotExist:
            return Response({'error': 'Object does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = user_serializer.UserSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 200,
                "data": serializer.data,
                "message": "Profile Updated Succesfully"
            })
        return Response({
            "status":400,
            "errors":serializer.errors,
            "message":"Something Went Wrong"
            })

# ################################################################   Pagination     ########################################################################################
class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })

# ################################################################   Categories     ########################################################################################
# All Categories With Pagination
class AllCategoryWithPagination(generics.ListAPIView):
    queryset = models.Categories.objects.all()
    serializer_class = admin_serializers.CategorySerializer
    pagination_class = CustomPageNumberPagination

# Particular Category Details
class CategoryDetails(APIView):
    def get(self, request, category_id):
        categories = models.Categories.objects.filter(id=category_id)
        serializer = admin_serializers.CategorySerializer(
            categories, many=True)
        return Response({
            'status': 200,
            'data': serializer.data,
            'message': 'success'
        })

# ################################################################   Sub Categories   ########################################################################################
# Fetch All Sub Categories for particular category
class ParticularCategoriesSubCategoriesList(APIView):
    def get(self, request, cat_id):
        sub_categories = models.SubCategories.objects.filter(category=cat_id)
        serializer = admin_serializers.SubCategorySerializer(sub_categories, many=True)
        return Response({
            'status': 200,
            'data': serializer.data,
            'message': 'success'
        })

# API View For Fetching all Sub Categories
class AllSubCategories(generics.ListAPIView):
    queryset = models.SubCategories.objects.all()
    serializer_class = admin_serializers.SubCategoryTableSerializer
    pagination_class = CustomPageNumberPagination

# All SubCategories According to category Along with all Products List
class AllProductsAccordingToSubCategory(APIView):
    def post(self, request, cat_id):
        # Get the subcategories queryset based on the provided category id
        sub_categories = models.SubCategories.objects.filter(category=cat_id).order_by('-id')
        # Create the serializer instance with the queryset and specify the context
        serializer = user_serializer.AllProductsAccordingToSubCategory(
            sub_categories, many=True, context={'request': request}
        )
        return Response({
            'status': 200,
            'data': serializer.data,
            'message': 'success'
        })


# ################################################################   Address   ########################################################################################
# Add Address
class AddAddress(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        address_serializer = user_serializer.AddressSerializer(data=request.data)
        if not address_serializer.is_valid():
            return Response({
                'status':400,
                'errors':address_serializer.errors,
                'message':'some error occurred'
            })
        else:
            address_serializer.save()
            return Response({
                'status':200,
                'data':address_serializer.data,
                'message':'Address Saved Succesfully'
            })

# Edit Address
class EditAddress(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        address_id = request.data['address_id']
        if models.Address.objects.filter(id=address_id):
            address = models.Address.objects.get(pk=address_id)
            address.area_street = request.data['area_street']
            address.city = request.data['city']
            address.full_name = request.data['full_name']
            address.hno = request.data['hno']
            # address.landmark = request.data['landmark']
            address.mobile = request.data['mobile']
            address.state = request.data['state']
            address.is_home = request.data['is_home']
            address.alternate_mobile = request.data['alternate_mobile']
            address.pincode = request.data['pincode']
            address.user = models.Users.objects.get(pk=request.data['user'])
            address.save()
            updated_address = models.Address.objects.filter(id=address_id)
            updated_address_serializer = user_serializer.AddressSerializer(updated_address,many=True)
            return Response({
                'status':200,
                'data':updated_address_serializer.data,
                'message':'Address Details Updated Succesfully'
            })
        else:
            return Response({
                'status':400,
                'message':'some error occurred'
            })

# Particular Users Address
class ParticularUsersAddress(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        user_id = request.data['user_id']
        address_list = models.Address.objects.filter(user = user_id)
        address_serialized_list = user_serializer.AddressSerializer(address_list,many=True)
        return Response({
            'status':200,
            'data':address_serialized_list.data,
            'message':'particular users addresses fetched'
        })

# Remove Address
class DeleteAddress(APIView):
    authentication_classes = [CustomAuthentication]
    def delete(self,request):
        address_id = request.data['address_id']
        if models.Address.objects.filter(id=address_id):
            address = models.Address.objects.get(pk=address_id)
            address.delete()
            return Response({
                'status':200,
                'bool':True,
                'message':'Address Removed Succesfully'
            })
        else:
            return Response({
                'status':400,
                'bool':False,
                'message':'No Address Found With This ID'
            })
        
# Particular address details
class ParticularAddressDetails(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        address_id = request.data['address_id']
        if models.Address.objects.filter(id=address_id):
            address = models.Address.objects.get(pk=address_id)
            address_serializer = user_serializer.AddressDetailedSerializer(address)
            return Response({
                'status':200,
                'data':address_serializer.data,
                'message':'Particular Address Details Fetched'
            })
        else:
            return Response({
                'status':400,
                'bool':False,
                'message':'No Address Found With This ID'
            })

################################################################### Products #################################################################
# API To Fetch All Products
class GetAllProducts(generics.ListAPIView):
    queryset = models.Product.objects.filter(is_visible = True).order_by('-id')
    serializer_class = admin_serializers.ProductComplteDetailsSerializer
    pagination_class = CustomPageNumberPagination
    def get_queryset(self):
        queryset = super().get_queryset()
        for product in queryset:
            product.calculate_rating()
        return queryset

# Particular Product Details
class ParticularProductDetails(APIView):
    def post(self,request):
        product_id = request.data['product_id']
        products = models.Product.objects.filter(id=product_id)
        for product in products:
            product.calculate_rating()  # Calculate the rating for each product
        product_serializer = user_serializer.ProductComplteDetailsWithReviews(products,many=True)
        return Response({
            'status':200,
            'data':product_serializer.data,
            'message':'All Products Fetched'
        })

################################################################### CART #################################################################
# API For Updating The Cart
class UpdateCart(APIView):
    def post(self,request):
        cart = models.Cart.objects.get(user = request.data['user'],product=request.data['product'])
        product = models.Product.objects.get(pk=cart.product.id)
        available_quantity = product.available_quantity
        if(request.data['quantity']<=available_quantity):
            cart.quantity = request.data['quantity']
            cart.size = request.data['size']
            cart.save()
            updated_cart = models.Cart.objects.filter(user = request.data['user'],product=request.data['product'])
            updated_cart_serializer = user_serializer.CartSerializer(updated_cart,many=True)
            return Response({
                'status':200,
                'errors':updated_cart_serializer.data,
                'message':'Cart Updated Succesfully'
            })
        else:
            return Response({
                'status':400,
                'available_auantity':available_quantity,
                'message':'Seller does not has enough stock'
            })

# Add Item To Cart
class AddItemToCart(APIView):
    def post(self,request):
        if models.Cart.objects.filter(user = request.data['user'],product=request.data['product']):
            cart = models.Cart.objects.get(user = request.data['user'],product=request.data['product'])
            product = models.Product.objects.get(pk=cart.product.id)
            available_quantity = product.available_quantity
            if(request.data['quantity']<=available_quantity): 
                cart.quantity = request.data['quantity']
                cart.save()
                updated_cart = models.Cart.objects.filter(user = request.data['user'],product=request.data['product'])
                updated_cart_serializer = user_serializer.CartDetailedSerializer(updated_cart,many=True)
                return Response({
                    'status':200,
                    'data':updated_cart_serializer.data,
                    'message':'Cart Updated Succesfully'
                })
            else:
                return Response({
                    'status':400,
                    'available_auantity':available_quantity,
                    'message':'Seller does not has enough stock'
                })
        else:
            if request.data['quantity']> models.Product.objects.get(pk=request.data['product']).available_quantity:
                return Response({
                    'status':400,
                    'available_auantity': models.Product.objects.get(pk=request.data['product']).available_quantity,
                    'message':'Seller does not has enough stock'
                })
            else:
                cart_serializer = user_serializer.CartSerializer(data=request.data)
                if not cart_serializer.is_valid():
                    return Response({
                        'status':400,
                        'errors':cart_serializer.errors,
                        'message':'some error occured'
                    })
                else:
                    cart_serializer.save()
                    updated_cart = models.Cart.objects.filter(id=cart_serializer.data['id'])
                    updated_cart_serializer = user_serializer.CartDetailedSerializer(updated_cart,many=True)
                    return Response({
                    'status':200,
                    'data':updated_cart_serializer.data,
                    'message':'Item added To Cart'
                })

# Particular Cart Details
class GetParticularCartDetails(APIView):
    def post(self,request):
        cart = models.Cart.objects.filter(user = request.data['user'],product=request.data['product'])
        cart_serializer = user_serializer.CartDetailedSerializer(cart,many=True)
        return Response({
            'status':200,
            'errors':cart_serializer.data,
            'message':'Cart Details Fetched Succesfully'
        })

# Particular Users Cart
class UsersCartDetails(APIView):
    def post(self,request):
        cart_items = models.Cart.objects.filter(user=request.data['user']).order_by('-id')
        cart_items_serializer = user_serializer.CartDetailedSerializer(cart_items,many=True)
        return Response({
            'status':200,
            'data':cart_items_serializer.data,
            'message':"Users Cart Fetched Succesfully"
        })

# Remove Item From Cart
class RemoveItemFromCart(APIView):
    def post(self,request):
        if models.Cart.objects.filter(user = request.data['user'],product=request.data['product']):
            cart_item = models.Cart.objects.get(user = request.data['user'],product=request.data['product'])
            cart_item.delete()
            return Response({
                    'status':200,
                    'bool':True,
                    'message':'Item Removed Succesfully'
                })
        else:
            return Response({
                'status':400,
                'bool':False,
                'message':'No Item Found With This ID'
            })

################################################################### Wishlist #################################################################
# Add Item To WishList
class AddToWhishlist(APIView):
    def post(self,request):
        if models.WishList.objects.filter(user=request.data['user'],product=request.data['product']):
            return Response({
                "status":200,
                "bool":False,
                "message":"Item Already Added to wishlist"
            })
        else:
            whishlist_serializer = user_serializer.UserWishlistSerializer(data=request.data)
            if not whishlist_serializer.is_valid():
                return Response({
                    'status':400,
                    'errors':whishlist_serializer.errors,
                    'message':'some error occured'
                })
            else:
                whishlist_serializer.save()
                return Response({
                'status':200,
                'data':whishlist_serializer.data,
                'message':'Item added To Wishlist'
            })

# Remove Item form WishList
class RemoveItemFromWishlist(APIView):
    def post(self,request):
        if models.WishList.objects.filter(product=request.data['product'],user=request.data['user']):
            wishlist_item = models.WishList.objects.get(product=request.data['product'],user=request.data['user'])
            wishlist_item.delete()
            return Response({
                    'status':200,
                    'bool':True,
                    'message':'Item Removed Succesfully'
                })
        else:
            return Response({
                'status':400,
                'bool':False,
                'message':'No Item Found With This ID'
            })

# Particular Users Wishlist
class ParticularUsersWishlist(APIView):
    def post(self,request):
        user_cart = models.WishList.objects.filter(user=request.data['user_id']).order_by('-id')
        user_cat_serializer = user_serializer.UserWishListCompleteSerializer(user_cart,many=True)
        return Response({
            'status':200,
            'data':user_cat_serializer.data,
            'message':'User Wishlist Details Fetched'
        })
    


# ###################################################################  Chat With Us ##########################################################################
# Add New Chat
class ChatWithus(APIView):
    # authentication_classes = [CustomAuthentication]
    def post(self,request):
        chat = user_serializer.ChatWithUsSerializer(data=request.data)
        if not chat.is_valid():
            return Response({
                'status':400,
                'errors':chat.errors,
                'message':'something went wrong'
            })
        else:
            chat.save()
            return Response({
                'status':200,
                'data':chat.data,
                'message':'Chat Sent Succesfully'
            })

# ###################################################################  Search Product  ##########################################################################
# Global Search for products which can retrieve products even when the keyword is matched in the description
class SearchProduct(APIView):
    def post(self, request, *args, **kwargs):
        query = request.data.get('query', '') # get the search query from the request data
        if query:
            queryset = models.Product.objects.filter(
                Q(description__icontains=query) | Q(product_title__icontains=query),is_visible =True
            )
            for product in queryset:
                product.calculate_rating()  # Calculate the rating for each product
            serializer = admin_serializers.ProductComplteDetailsSerializer(queryset, many=True)
            return Response({
                'status':200,
                'data':serializer.data,
                'message':'products fetched'
            })
        else:
            query = "!!!----"
            queryset = models.Product.objects.filter(
                Q(description__icontains=query) | Q(product_title__icontains=query),is_visible =True
            )
            for product in queryset:
                product.calculate_rating()  # Calculate the rating for each product
            serializer = admin_serializers.ProductComplteDetailsSerializer(queryset, many=True)
            return Response({
                'status':200,
                'data':serializer.data,
                'message':'products fetched'
            })

#############################################################   User Reviews   #####################################################################
# Post A Review
class PostReview(APIView):
    def post(self,request):
        review_serializer = user_serializer.ReviewSerializer(data = request.data)
        if not review_serializer.is_valid():
            return Response({
                'status': 403,
                'errors': review_serializer.errors,
                'message': 'Some Error Occurred'
            })
        else:
            review_serializer.save()
            return Response({
                'status': 200,
                'data': review_serializer.data,
                'message': 'Review Posted Succesfully'
            })

# Particular Products All Reviews
class ParticularProductReviews(APIView):
    def get(self,request,product_id):
        product_reviews = models.Reviews.objects.filter(product_id=product_id)
        product_reviews_serializer = user_serializer.ReviewDetailedSerializer(product_reviews,many=True)
        return Response({
            'status': 200,
            'data': product_reviews_serializer.data,
            'message': 'All Reviews Fetched Succesfully'
        })

# Edit A Particular Review
class DeleteReview(APIView):
    def delete(self,request,review_id):
        if models.Reviews.objects.filter(id = review_id):
            review = models.Reviews.objects.get(pk = review_id)
            review.delete()
            return Response({
                'status': 200,
                'bool':True,
                'message': 'Review Deleted Succesfully'
            })
        else:
            return Response({
                'status': 400,
                'bool':False,
                'message': 'Review With This Already Deleted'
            })

#############################################################   Coupons   #####################################################################
# Fetch All Coupons With Token
class GetCoupons(APIView):
    # authentication_classes = [CustomAuthentication]
    def get(self,request):
        coupons = models.Coupons.objects.all()
        serializer = admin_serializers.CounponsSerializer(coupons,many=True)
        return Response({
            'status': 200,
            'data': serializer.data,
            'message': 'success'
        })

# Get Particular Coupon
class ParticularCouponDetails(APIView):
    # authentication_classes = [CustomAuthentication]
    def get(self,request):
        coupons = models.Coupons.objects.filter(id=request.data['coupon_id'])
        serializer = admin_serializers.CounponsSerializer(coupons,many=True)
        return Response({
            'status': 200,
            'data': serializer.data,
            'message': 'success'
        })

#############################################################   Orders   #####################################################################
# Placing An Order By End User
class CreateOrders(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        order_serializer = user_serializer.OrdersSerializer(data= request.data)
        if not order_serializer.is_valid():
            return Response({
                'status': 403,
                'errors': order_serializer.errors,
                'message': 'Some Error Occurred'
            })
        else:
            order_serializer.save()
            return Response({
                'status': 200,
                'data': order_serializer.data,
                'message': 'Order Placed Succesfully'
            })

class OrderDetails(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self, request):
        order_id = request.data['order_id']
        order_details = models.OrderModel.objects.get(id=order_id)
        order_details_serializer = user_serializer.OrderTrackingDetails(order_details)
        return Response({
            'status': 200,
            'data': order_details_serializer.data,
            'message': 'Order Details Fetched Successfully'
        })

# Orders History
class ParticularUserOrdersHistory(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        particular_users_orders = models.OrderModel.objects.filter(user_id = request.data['user']).order_by('-id')
        users_orders_serializer = user_serializer.OrderDetailsWithOrderItems(particular_users_orders,many=True)
        return Response({
            'status': 200,
            'data': users_orders_serializer.data,
            'message': 'Order History Fetched Succesfully'
        })

# Adding Order Items to the order
class AddOrderItems(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self, request):
        if request.data['quantity'] > models.Product.objects.get(pk=request.data['product']).available_quantity :
            return Response({
                "status":400,
                "bool":False,
                "message":"Insufficient Products"
            })
        order_serializer = user_serializer.OrderItemsSerializer(data=request.data)
        if not order_serializer.is_valid():
            return Response({
                'status': 400,
                'errors': order_serializer.errors,
                'message': 'some error occurred'
            })
        else:
            order_serializer.save()
            product = models.Product.objects.get(pk=request.data['product'])
            product.no_of_orders = product.no_of_orders + 1
            return Response({
                'status': 200,
                'data': order_serializer.data,
                'message': 'Order Items Saved Succesfully'
            })

# Empty Users Cart
class EmptyUsersCart(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        cart = models.Cart.objects.filter(user = request.data['user'])
        if cart:
            for c in cart:
                c.delete()
            return Response({
                'status':200,
                'message':'deleted users cart'
            })
        else:
            return Response({
                'status':400,
                'message':'No Items in Users Cart'
            })

# Mostly Liked
class TopSellingProducts(APIView):
    # authentication_classes = [CustomAuthentication]
    def get(self,request):
        products = models.Product.objects.filter(is_visible =True).order_by('no_of_orders').reverse()
        for product in products:
            product.calculate_rating()  # Calculate the rating for each product
        product_serializer = admin_serializers.ProductComplteDetailsSerializer(products,many=True)
        return Response({
            'status':200,
            'data':product_serializer.data
        })

# Request For Order Cancellation
class RequestForOrderCancellation(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        order=models.OrderModel.objects.get(pk=request.data["order_id"])
        order.order_status="20"
        order.save()
        return Response({
            'status':200,
            'message': "order cancel request sent"
        })

# Request for Returning Order
class RequestForReturn(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        orders=models.OrderModel.objects.get(pk=request.data['order_id'])
        orders.order_status="10"
        orders.save()
        return Response ({
            'status':200,
            'message':"Request for order return"
        })

###########################################################################################################################################################################
# #############################################################################   Phase - 2   #############################################################################
# ###########################################################              Customizer Views Start                  ########################################################
###########################################################################################################################################################################
# All Fonts API
class AllCustomizerGET(APIView):
    def get(self,request):
        fonts = models.CustomizerFonts.objects.all().order_by('-id')
        fonts_serializer = admin_serializers.FontsSerializer(fonts,many=True)
        emojis = models.CustomizerEmojis.objects.all().order_by('-id')
        emojis_serializer = admin_serializers.EmojiSerializer(emojis,many=True)
        colors = models.CustomizerColors.objects.all().order_by('-id')
        colors_serializer = admin_serializers.CustomizerColorsSerializers(colors,many=True)
        shapes = models.CustomizerShapes.objects.all().order_by('-id')
        shapes_serializer = admin_serializers.CustomizerShapesSerializer(shapes,many=True)
        bg_images = models.CustomizerBackgroundimages.objects.all().order_by('-id')
        bg_imgs_serializer = admin_serializers.CustomizerBackgroundImagesSerializer(bg_images,many=True)
        dimensions = models.CustomizerDimensions.objects.all().order_by('-id')
        dimensions_serializer = admin_serializers.CustomizerDimensionsSerializer(dimensions,many=True)
        return Response({
            "status":200,
            "fonts":fonts_serializer.data,
            "emojis":emojis_serializer.data,
            "colors":colors_serializer.data,
            "shapes":shapes_serializer.data,
            "dimensions":dimensions_serializer.data,
            "data":bg_imgs_serializer.data,
            "message":"All Customizer GET Data Fetched"
        })

# NewCustomizer 
class NewCustomizer(APIView):
    def post(self,request):
        new_customizer_seializer = user_serializer.NewCustomizer(data=request.data)
        if new_customizer_seializer.is_valid():
            new_customizer_seializer.save()
            return Response({
                "status":200,
                "data":new_customizer_seializer.data,
                "message":"New Customizer Saved Successfully"
            })
        else:
            return Response({
                "status":400,
                "errors":new_customizer_seializer.errors,
                "message":"Some Error Occurred"
            })
       
# ###########################################################              Place Order For Customizer                  ########################################################
# Class Place New Order For Customizer
class CreateOrdersForCustomizer(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        order_serializer = user_serializer.PlaceOrderForCustomizedProduct(data= request.data)
        if not order_serializer.is_valid():
            return Response({
                'status': 403,
                'errors': order_serializer.errors,
                'message': 'Some Error Occurred'
            })
        else:
            order_serializer.save()
            return Response({
                'status': 200,
                'data': order_serializer.data,
                'message': 'Order Placed Succesfully'
            })

class OrderDetailsForCustomizer(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self, request):
        order_id = request.data['order_id']
        order_details = models.PlaceOrderForCustomizedProducts.objects.get(id=order_id)
        order_details_serializer = user_serializer.OrderDetailsForCustomizer(order_details)
        return Response({
            'status': 200,
            'data': order_details_serializer.data,
            'message': 'Order Details Fetched Successfully'
        })

# Orders History
class ParticularUserOrdersHistoryForCustomizer(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        particular_users_orders = models.PlaceOrderForCustomizedProducts.objects.filter(user_id = request.data['user_id']).order_by('-id')
        users_orders_serializer = user_serializer.OrderDetailsForCustomizer(particular_users_orders,many=True)
        return Response({
            'status': 200,
            'data': users_orders_serializer.data,
            'message': 'Order History Fetched Succesfully'
        })

# Request For Order Cancellation For Customizers
class CustomizerOrderRequestForOrderCancellation(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        order=models.PlaceOrderForCustomizedProducts.objects.get(pk=request.data["order_id"])
        order.order_status="20"
        order.save()
        return Response({
            'status':200,
            'message': "order cancel request sent"
        })

# Request for Returning Order
class CustomizerOrderRequestForReturn(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        orders=models.PlaceOrderForCustomizedProducts.objects.get(pk=request.data['order_id'])
        orders.order_status="10"
        orders.save()
        return Response ({
            'status':200,
            'message':"Request for order return"
        })

# ###########################################################              Customizable Templates                  ########################################################
# GET All Customizable Templates
class AllTemplates(APIView):
    def get(self,request):
        templates = models.CustomizableLogoTemplates.objects.all().order_by('-id')
        template_serializer = admin_serializers.TemplateSerializer(templates,many=True)
        return Response({
            "status":200,
            "data":template_serializer.data,
            "message":"All Templates Fetched Succesfully"
        })

# POST Place Order For Logo Template
class CreateOrdersForLogoTemplate(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        order_serializer = user_serializer.PlaceOrderSerializerForLogoTemplate(data= request.data)
        if order_serializer.is_valid():
            order_serializer.save()
            return Response({
                'status': 200,
                'data': order_serializer.data,
                'message': 'Order Placed Succesfully'
            })
        else:
            return Response({
                'status': 403,
                'errors': order_serializer.errors,
                'message': 'Some Error Occurred'
            })

class OrderDetailsForLogoTemplate(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self, request):
        order_id = request.data['order_id']
        order_details = models.PlaceOrderForLogoTemplate.objects.get(id=order_id)
        order_details_serializer = user_serializer.OrderDetailsForLogo(order_details)
        return Response({
            'status': 200,
            'data': order_details_serializer.data,
            'message': 'Order Details Fetched Successfully'
        })

# Orders History
class ParticularUserOrdersHistoryForLogo(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        particular_users_orders = models.PlaceOrderForLogoTemplate.objects.filter(user_id = request.data['user_id']).order_by('-id')
        users_orders_serializer = user_serializer.OrderDetailsForLogo(particular_users_orders,many=True)
        return Response({
            'status': 200,
            'data': users_orders_serializer.data,
            'message': 'Order History Fetched Succesfully'
        })

# Request For Order Cancellation For Customizers
class LogoOrderRequestForOrderCancellation(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        order=models.PlaceOrderForLogoTemplate.objects.get(pk=request.data["order_id"])
        order.order_status="20"
        order.save()
        return Response({
            'status':200,
            'message': "order cancel request sent"
        })

# Request for Returning Order
class LogoOrderRequestForReturn(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        orders=models.PlaceOrderForLogoTemplate.objects.get(pk=request.data['order_id'])
        orders.order_status="10"
        orders.save()
        return Response ({
            'status':200,
            'message':"Request for order return"
        })





# # Delete Entire Users Wishlist
# class EmptyUsersWishList(APIView):
#     def post(self,request):
#         user_cart = models.WishList.objects.filter(user=request.data['user_id'])
#         user_cart.delete()
#         return Response({
#             'status':200,
#             'message':'User Cart Deleted Succesfully'
#         })




