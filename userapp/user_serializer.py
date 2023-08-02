from rest_framework import serializers
from maintribe import models
import uuid
import random
from rest_framework.serializers import ValidationError

# End User Serializer
class UserSerializer(serializers.ModelSerializer):
    profile = serializers.ImageField(required=False, allow_null=True, default="")
    firebase_id = serializers.CharField(allow_blank=True)
    class Meta:
        model = models.Users
        fields = '__all__'
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'profile' not in data or data['profile'] is None:
            data['profile'] = ''
        return data
    def create(self, validated_data):
        otp_generated = random.randint(10000, 99999)
        phone = validated_data['phone']

        if models.Users.objects.filter(phone=phone).exists():
            user = models.Users.objects.get(phone=phone)
            user.otp = otp_generated
            user.save()
        else:
            user = models.Users.objects.create(
                firebase_id=validated_data['firebase_id'],
                otp=otp_generated,
                name=validated_data['name'],
                email=validated_data['email'],
                phone=validated_data['phone'],
                uid=uuid.uuid4(),
                device_id=validated_data['device_id']
            )
        return user

# Address Serializer
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = "__all__"
    def create(self,validated_data):
        address = models.Address.objects.create(user=validated_data['user'],full_name=validated_data['full_name'],mobile=validated_data['mobile'],hno=validated_data['hno'],area_street=validated_data['area_street'],alternate_mobile=validated_data['alternate_mobile'],pincode =validated_data['pincode'],city=validated_data['city'],state=validated_data['state'],is_home = validated_data['is_home'])
        address.save()
        return address

# Detailed Address Serializzer
class AddressDetailedSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = models.Address
        fields ="__all__"
        depth = 2

# CART Serializer
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = "__all__"
    def create(self, validated_data):
        product = models.Product.objects.get(pk=validated_data['product'].id)
        available_quantity = product.available_quantity
        if validated_data['quantity'] <= available_quantity:
            cart = models.Cart.objects.create(color=validated_data['color'],is_controller=validated_data['is_controller'],user=validated_data['user'],product=validated_data['product'],quantity=validated_data['quantity'],size=validated_data['size'])
            cart.save()
            return cart
        else:
            raise ValidationError('Seller Doent Have Enough Stock')
            
# CART Detailed Serializer With User and Product Objects
class CartDetailedSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = models.Cart
        fields = "__all__"
        depth = 2
    def get_user(self, obj):
        user = obj.user
        profile = user.profile or ""  # Check if profile exists, otherwise set it to an empty string
        user_data = UserSerializer(user).data
        user_data['profile'] = profile
        return user_data
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_data = representation.get('user')
        if user_data:
            user_data['profile'] = user_data['profile'] or ""  # Set profile field to empty string if it is None
        return representation

# Users Wishlist Serializer
class UserWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WishList
        fields="__all__"
    def create(self,validated_data):
        whishlist = models.WishList.objects.create(color=validated_data['color'],size=validated_data['size'],user=validated_data['user'],product=validated_data['product'])
        whishlist.save()
        return whishlist

# Users Wishlist With Product Images and Product Details
class UserWishListCompleteSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = models.WishList
        fields = "__all__"
        depth = 2

# Chat With us Serializer for enduser
class ChatWithUsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = models.ChatWithus
        fields = "__all__"
    def create(self,validated_data):
        chatWithUs = models.ChatWithus.objects.create(user=validated_data['user'],text=validated_data['text'])
        chatWithUs.save()
        return chatWithUs

# End User Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reviews
        fields = "__all__"
    def create(self, validated_data):
        review = models.Reviews.objects.create(user=validated_data['user'], product=validated_data['product'], subject=validated_data['subject'], description=validated_data['description'],ratings=validated_data['ratings'])
        review.save()
        return review

# Reviews Detailed Serializer
class ReviewDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reviews
        fields = "__all__"
        depth = 1

# End User Orders Serializer
class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderModel
        fields = "__all__"
    def create(self, validated_data):
        orders = models.OrderModel.objects.create(**validated_data)
        return orders
    
# Serializer for Adding Products To The Order Model
class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.OrderItems
        fields='__all__'
    def create(self,validated_data):
        product = models.Product.objects.get(pk=validated_data['product'].id)
        if product.available_quantity < validated_data['quantity']:
            raise serializers.ValidationError("Not Enough Products")
        else:
            items=models.OrderItems.objects.create(size=validated_data['size'],color=validated_data['color'],quantity=validated_data['quantity'],product=validated_data['product'],order=validated_data['order'])
            product.no_of_orders = product.no_of_orders+1
            product.save()
            items.save()
            return items

# Serializer for handling the product Images
class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductColorImages
        fields = "__all__"
    def create(self, validated_data):
        image_product = models.ProductColorImages.objects.create(product = validated_data['product'],image =validated_data['image'])
        image_product.save()
        return image_product

# Complete Product Serializer
class ProductComplteDetailsSerializer(serializers.ModelSerializer):
    product_images = ProductImagesSerializer(many=True,read_only = True)
    discount_1 = serializers.SerializerMethodField()
    discount_2 = serializers.SerializerMethodField()
    discount_3 = serializers.SerializerMethodField()
    discount_4 = serializers.SerializerMethodField()
    discount_5 = serializers.SerializerMethodField()
    class Meta:
        model = models.Product
        fields = "__all__"
        depth = 1
    def get_discount_1(self, obj):
        if obj.size_actual_price_1 and obj.size_selling_price_1:
            discount = ((obj.size_actual_price_1 - obj.size_selling_price_1) / obj.size_actual_price_1) * 100
            return round(discount, 2)
        return 0
    def get_discount_2(self, obj):
        if obj.size_actual_price_2 and obj.size_selling_price_2:
            discount = ((obj.size_actual_price_2 - obj.size_selling_price_2) / obj.size_actual_price_2) * 100
            return round(discount, 2)
        return 0
    def get_discount_3(self, obj):
        if obj.size_actual_price_3 and obj.size_selling_price_3:
            discount = ((obj.size_actual_price_3 - obj.size_selling_price_3) / obj.size_actual_price_3) * 100
            return round(discount, 2)
        return 0
    def get_discount_4(self, obj):
        if obj.size_actual_price_4 and obj.size_selling_price_4:
            discount = ((obj.size_actual_price_4 - obj.size_selling_price_4) / obj.size_actual_price_4) * 100
            return round(discount, 2)
        return 0
    def get_discount_5(self, obj):
        if obj.size_actual_price_5 and obj.size_selling_price_5:
            discount = ((obj.size_actual_price_5 - obj.size_selling_price_5) / obj.size_actual_price_5) * 100
            return round(discount, 2)
        return 0

# Product Reviews Serializer
class ProductReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reviews
        fields = "__all__"

# Complete Product Serializer With Reviews
class ProductComplteDetailsWithReviews(serializers.ModelSerializer):
    product_images = ProductImagesSerializer(many=True,read_only = True)
    product_reviews = ProductReviewsSerializer(many=True,read_only = True)
    class Meta:
        model = models.Product
        fields = "__all__"
        depth = 1


# # All Products With Subcategory
class AllProductsAccordingToSubCategory(serializers.ModelSerializer):
    sub_cat_product = ProductComplteDetailsSerializer(many=True, read_only=True)
    class Meta:
        model = models.SubCategories
        fields = "__all__"
        depth = 1
    def to_representation(self, instance):
        sub_category = super().to_representation(instance)
        visible_products = models.Product.objects.filter(sub_category=instance, is_visible=True)
        visible_products_serializer = ProductComplteDetailsSerializer(visible_products, many=True)
        sub_category['sub_cat_product'] = visible_products_serializer.data
        return sub_category


# Product Serializer
class PrpductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"
    def create(self,validated_data):
        product = models.Product.objects.create(width=validated_data['width'],height=validated_data['height'],weight=validated_data['weight'],color=validated_data['color'],font=validated_data['font'],available_quantity=validated_data['available_quantity'],selling_price=validated_data['selling_price'],actual_price=validated_data['actual_price'],sku_code = validated_data['sku_code'],sub_category = validated_data['sub_category'],category = validated_data['category'],description=validated_data['description'],product_title = validated_data['product_title'])
        product.save()
        return product

# Detailed Order Items Serializer
class OrderItemsDetailedSerializer(serializers.ModelSerializer):
    product = PrpductSerializer()
    class Meta:
        model = models.OrderItems
        fields = "__all__"
        depth = 2 

# Detailed Orders Serializer Along With Ordered Items, User, Address, Coupon Objects
class OrderDetailsWithOrderItems(serializers.ModelSerializer):
    order_items = OrderItemsDetailedSerializer(many=True,read_only = True)
    user = UserSerializer()
    address = AddressDetailedSerializer()
    class Meta:
        model = models.OrderModel
        fields = "__all__"
        depth = 2
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if 'coupon' in representation and representation['coupon'] is None:
            representation['coupon'] = ""
        return representation

# Order Items Serializer For Order Tracing 
class OrderItemsForOrderTracking(serializers.ModelSerializer):
    product = ProductComplteDetailsSerializer()
    class Meta:
        model=models.OrderItems
        fields='__all__'

# Detailed Orders Serializer For Order Tracking
class OrderTrackingDetails(serializers.ModelSerializer):
    order_items = OrderItemsForOrderTracking(many=True,read_only = True)
    class Meta:
        model = models.OrderModel
        fields = "__all__"
        depth = 2
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if 'coupon' in representation and representation['coupon'] is None:
            representation['coupon'] = ""
        return representation

#############################################################################   Phase - 2   #############################################################################
# Customizer Place Order
class NewCustomizer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomizedProduct
        fields = "__all__"
    def create(self, validated_data):
        new_customizer_product = models.CustomizedProduct.objects.create(**validated_data)
        new_customizer_product.save()
        return new_customizer_product

# PlaceOrder For Customized Product
class PlaceOrderForCustomizedProduct(serializers.ModelSerializer):
    class Meta:
        model = models.PlaceOrderForCustomizedProducts
        fields = "__all__"
    def create(self,validated_data):
        new_order_for_customizer = models.PlaceOrderForCustomizedProducts(**validated_data)
        new_order_for_customizer.save()
        return new_order_for_customizer

# Detailed Place Order For Customizer
class DetailedCustomizerOrders(serializers.ModelSerializer):
    class Meta:
        model = models.PlaceOrderForCustomizedProducts
        fields = "__all__"
        depth = 2
    
# Complete Order Details 
class OrderDetailsForCustomizer(serializers.ModelSerializer):
    user = UserSerializer()
    address = AddressDetailedSerializer()
    class Meta:
        model = models.PlaceOrderForCustomizedProducts
        fields = "__all__"
        depth = 2

#############################################################################   Logo Templates   #############################################################################
class PlaceOrderSerializerForLogoTemplate(serializers.ModelSerializer):
    template_product = serializers.PrimaryKeyRelatedField(queryset=models.CustomizableLogoTemplates.objects.all(), write_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset = models.Users.objects.all(),write_only=True)
    class Meta:
        model = models.PlaceOrderForLogoTemplate
        fields = "__all__"
        depth = 2

    def create(self, validated_data):
        template_product = validated_data.pop('template_product')
        new_order_for_logo_template = models.PlaceOrderForLogoTemplate(template_product=template_product, **validated_data)
        new_order_for_logo_template.save()
        return new_order_for_logo_template

# Complete Order Details 
class OrderDetailsForLogo(serializers.ModelSerializer):
    user = UserSerializer()
    address = AddressDetailedSerializer()
    class Meta:
        model = models.PlaceOrderForLogoTemplate
        fields = "__all__"
        depth = 2

# Detailed Place Order For Logo Template
class DetailedLogoTemplateOrders(serializers.ModelSerializer):
    class Meta:
        model = models.PlaceOrderForLogoTemplate
        fields = "__all__"
        depth = 2































