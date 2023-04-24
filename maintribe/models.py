from django.db import models
import uuid



# States API
class States(models.Model):
    state_name = models.CharField(max_length=250)
    state_representing_image = models.ImageField(
        upload_to='states/', null=True)
    def __str__(self):
        return str(self.id) + "." + self.state_name
    class Meta:
        verbose_name_plural = "1.States"


# Districts API
class Districts(models.Model):
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    district_name = models.CharField(max_length=250)
    def __str__(self):
        return str(self.id) + "." + self.district_name
    class Meta:
        verbose_name_plural = "2.districts"


# Mandal API
class Mandal(models.Model):
    district = models.ForeignKey(Districts, on_delete=models.CASCADE)
    mandal_name = models.CharField(max_length=200)
    def __str__(self):
        return str(self.id)+"."+self.mandal_name
    class Meta:
        verbose_name_plural = "3.Mandal"


# UserBase Model
class UserBaseModel(models.Model):
    id = models.CharField(default ="", max_length=100)
    uid = models.UUIDField(primary_key=True, editable=False,default = uuid.uuid4())
    created_date = models.DateField(auto_now_add=True)
    created_time= models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)
    class Meta:
        abstract = True

#############################################################   Super Admin Models   #####################################################################
# Super Admin Account
class SuperAdminAcc(models.Model):
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=200)
    def __str__(self):
        return self.username

# Categories
class Categories(models.Model):
    category = models.CharField(max_length=200)
    category_image = models.ImageField(upload_to="category_images/")
    def __str__(self):
        return self.category

# Sub Categories
class SubCategories(models.Model):
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=200)
    def __str__(self):
        return self.sub_category

# Products
class Product(models.Model):
    # Product Details
    product_title = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategories,on_delete=models.CASCADE,related_name="sub_cat_product")
    sku_code = models.CharField(max_length=200,unique=True)
    thumbnail = models.ImageField(upload_to='product_thumbnail/')
    # product Sizes_prices
    # Size -1
    size_lable_1 = models.CharField(max_length=200)
    size_height_1 = models.CharField(max_length=200)
    size_width_1 = models.CharField(max_length=200)
    size_actual_price_1 = models.FloatField()
    size_selling_price_1 = models.FloatField()
    # Size-2
    size_lable_2 = models.CharField(max_length=200,null=True)
    size_height_2 = models.CharField(max_length=200,null=True)
    size_width_2 = models.CharField(max_length=200,null=True)
    size_actual_price_2 = models.FloatField(null=True)
    size_selling_price_2 = models.FloatField(null=True)
    # Size-3
    size_lable_3 = models.CharField(max_length=200,null=True)
    size_height_3 = models.CharField(max_length=200,null=True)
    size_width_3 = models.CharField(max_length=200,null=True)
    size_actual_price_3 = models.FloatField(null=True)
    size_selling_price_3 = models.FloatField(null=True)
    # Size-4
    size_lable_4 = models.CharField(max_length=200,null=True)
    size_height_4 = models.CharField(max_length=200,null=True)
    size_width_4 = models.CharField(max_length=200,null=True)
    size_actual_price_4 = models.FloatField(null=True)
    size_selling_price_4 = models.FloatField(null=True)
    # Size-5
    size_lable_5 = models.CharField(max_length=200,null=True)
    size_height_5 = models.CharField(max_length=200,null=True)
    size_width_5 = models.CharField(max_length=200,null=True)
    size_actual_price_5 = models.FloatField(null=True)
    size_selling_price_5 = models.FloatField(null=True)
    # product Status
    stock_status = models.CharField(max_length=500,default="Available")
    available_quantity = models.IntegerField()
    no_of_wishlists = models.IntegerField(default=0)
    no_of_cart = models.IntegerField(default=0)
    no_of_returned = models.IntegerField(default=0)
    # Product Posted Details
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)

# Product Images and colors
class ProductColorImages(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_images')
    image = models.ImageField(upload_to="product_images/")
    color_name = models.CharField(max_length=200)
    color_code = models.CharField(max_length=200)

# Stories
class HighlightStories(models.Model):
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='story_thumbnail/')
    img_video = models.FileField(max_length=200,upload_to='stories/')
    type=models.CharField(max_length=200,default="image")
    # Story Posted Details
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)

# Banners
class Banners(models.Model):
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    banner=models.ImageField(max_length=200,upload_to='banners/')
    date=models.DateField(auto_now_add=True)
    time=models.TimeField(auto_now_add=True)


















#############################################################   End User Models   #####################################################################

class UserBaseModel(models.Model):
    id = models.CharField(default ="", max_length=100)
    uid = models.UUIDField(primary_key=True, editable=False,default = uuid.uuid4())
    created_date = models.DateField(auto_now_add=True)
    created_time= models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)
    class Meta:
        abstract = True

# User Model
class Users(UserBaseModel):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=200,default="", null=True)
    phone = models.CharField(max_length=100)
    otp = models.CharField(max_length=10,default="00000")
    profile = models.ImageField(upload_to='profile_pictures/',null=True)
    device_id = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return self.phone

# Address 
class Address(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    state = models.CharField(max_length=500)
    full_name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=200)
    hno = models.CharField(max_length=500)
    area_street = models.CharField(max_length=200)
    landmark = models.CharField(max_length=500)
    pincode = models.CharField(max_length=200)
    city = models.CharField(max_length=500)

# Orders
class Orders(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchased_price = models.CharField(max_length=200)
    created_date = models.DateField(auto_now_add=True)
    created_time= models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)

# CART
class Cart(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(default='1',max_length=200)

# Wishlist
class WishList(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

# Chat With Us For EndUser
class ChatWithus(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    created_date = models.DateField(auto_now_add=True)
    created_time= models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)

# Replies By Admin To Chat With us
class ChatWithUsReply(models.Model):
    userChat_id = models.ForeignKey(ChatWithus,on_delete=models.CASCADE)
    reply_text = models.CharField(max_length=500)
    created_date = models.DateField(auto_now_add=True)
    created_time= models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)

# Coupons
class Coupons(models.Model):
    coupon_code = models.CharField(max_length=200)
    coupon_description = models.TextField()
    discount_percentage = models.IntegerField()
    min_price_for_coupon_avail = models.IntegerField()
    max_price = models.IntegerField()
    no_of_days_valid = models.CharField(max_length=200)
    no_of_coupons = models.IntegerField()

    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)
    def __str__(self):
        return self.coupon_code

# Reviews
class Reviews(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    subject = models.CharField(max_length=200,null=True)
    description = models.TextField()
    ratings = models.IntegerField()
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)



# Orders API
# class PlaceOrder(models.Model):
#     product = models.ForeignKey(Product,on_delete=models.CASCADE)
#     product_quantity = models.IntegerField()
#     user =models.ForeignKey(Users,on_delete=models.CASCADE)
#     address = models.ForeignKey(Address,on_delete=models.CASCADE)
#     is_coupon_applied = models.BooleanField(default=False)
#     purchased_amount = models.IntegerField()

#     created_date = models.DateField(auto_now_add=True)
#     created_time = models.TimeField(auto_now_add=True)
#     updated_date = models.DateField(auto_now=True)
#     updated_time = models.TimeField(auto_now=True)





    