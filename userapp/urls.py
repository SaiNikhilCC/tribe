from django.urls import path
from . import views

urlpatterns = [
    # USER REGISTRATION AND VERIFYING OTP
    path('register-user/', views.RegisterUser.as_view()),
    path('verify-otp/',views.VerifyOtp.as_view()),
    path('resend-otp/',views.ResendOTP.as_view()),
    path('login/',views.Login.as_view()),
    path('user-profile/',views.UserProfile.as_view()),
    path('edit-user-profile/',views.EditUserProfile.as_view()),
    # Categories
    path("all-category/",views.AllCategoryWithPagination.as_view()),
    path("category-details/<int:category_id>/",views.CategoryDetails.as_view()),
    # Sub Categories
    path("particular-category-sub-category-list/<int:cat_id>/",views.ParticularCategoriesSubCategoriesList.as_view()),
    path("all-sub-categories/",views.AllSubCategories.as_view()),
    path("all-sub-categories-posts/<int:cat_id>/",views.AllProductsAccordingToSubCategory.as_view()),
    # Add Address
    path('add-address/',views.AddAddress.as_view()),
    path('edit-address/',views.EditAddress.as_view()),
    path('particular-user-all-address/',views.ParticularUsersAddress.as_view()),
    path('remove-address/',views.DeleteAddress.as_view()),
    path('particular-address-details/',views.ParticularAddressDetails.as_view()),
    # Products
    path('get-all-products/',views.GetAllProducts.as_view()),
    path('particular-product-details/',views.ParticularProductDetails.as_view()),
    # Search Product
    path("products/",views.SearchProduct.as_view()),
    # CART
    path('add-item-to-cart/',views.AddItemToCart.as_view()),
    path('update-cart/',views.UpdateCart.as_view()),
    path('particular-cart-details/',views.GetParticularCartDetails.as_view()),
    path('get-users-cart/',views.UsersCartDetails.as_view()),
    path('remove-item-from-cart/',views.RemoveItemFromCart.as_view()),
    # Wishlist
    path('add-to-wishlist/',views.AddToWhishlist.as_view()),
    path('get-users-wishlist/',views.ParticularUsersWishlist.as_view()),
    path('remove-from-wishlist/',views.RemoveItemFromWishlist.as_view()),
    # Orders
    path("create-order/",views.CreateOrders.as_view()),
    path("order-details/",views.OrderDetails.as_view()),
    path("particular-user-orders-history/",views.ParticularUserOrdersHistory.as_view()),
    path('add-order-items/',views.AddOrderItems.as_view()),
    # Chat With Us
    path('chat-with-us/',views.ChatWithus.as_view()),
    # Reviews
    path("post-review/",views.PostReview.as_view()),
    path("particular-product-reviews/<int:product_id>/",views.ParticularProductReviews.as_view()),
    path("delete-review/<int:review_id>/",views.DeleteReview.as_view()),
    # Coupons
    path("get-coupons/",views.GetCoupons.as_view()),
    path("get-coupon-details/",views.ParticularCouponDetails.as_view()),
    # Empty Users Cart
    path("empty-users-cart/",views.EmptyUsersCart.as_view()),
    # Top Selling Products
    path("top-selling-products/",views.TopSellingProducts.as_view()),
    # Request for Order Cancellation
    path('request-for-order-cancellation/',views.RequestForOrderCancellation.as_view()),
    # Request for Returning Order
    path('request-order-return/',views.RequestForReturn.as_view()),

    
    # #############################################################################   Phase - 2   #############################################################################
    # Customizer Fonts
    path("all-customizer-get/",views.AllCustomizerGET.as_view()),
    # New Customizer
    path("new-customizer/",views.NewCustomizer.as_view()),
    # Orders For Customizer
    path("place-new-order-customizer/",views.CreateOrdersForCustomizer.as_view()),
    path("particular-order-details-for-customizer/",views.OrderDetailsForCustomizer.as_view()),
    path("particular-user-all-order-for-customizer/",views.ParticularUserOrdersHistoryForCustomizer.as_view()),
    path("customizer-order-request-for-order-cancellation/",views.CustomizerOrderRequestForOrderCancellation.as_view()),
    path('customizer-order-request-order-return/',views.CustomizerOrderRequestForReturn.as_view()),

    # ALl Templates
    path("all-templates/",views.AllTemplates.as_view()),
    # Orders For Customizer
    path("place-order-logo-template/",views.CreateOrdersForLogoTemplate.as_view()),
    path("particular-order-details-for-logo/",views.OrderDetailsForLogoTemplate.as_view()),
    path("particular-user-all-order-for-logo/",views.ParticularUserOrdersHistoryForLogo.as_view()),
    path("logo-order-request-for-order-cancellation/",views.LogoOrderRequestForOrderCancellation.as_view()),
    path('logo-order-request-order-return/',views.LogoOrderRequestForReturn.as_view()),


    # # Empty Users Wishlist
    # path("empty-users-wishlist/",views.EmptyUsersWishList.as_view()),

]



