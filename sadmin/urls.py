from django.urls import path
from . import views

urlpatterns = [
    # Super Admin Login API View
    path("login/",views.SuperAdminLoginView.as_view()),
    # Categories
    path("add-category/",views.AddCategory.as_view()),
    path("all-category/",views.AllCategory.as_view()),
    path("category-details/<int:category_id>/",views.CategoryDetails.as_view()),
    path("edit-category/<int:category_id>/",views.EditCategory.as_view()),
    path("delete-category/<int:category_id>/",views.DeleteCategory.as_view()),
    # Sub Caategories
    path("add-sub-category/",views.SubCategory.as_view()),
    path("particular-category-sub-category-list/<int:cat_id>/",views.ParticularCategoriesSubCategoriesList.as_view()),
    path("particular-category-sub-category-table/<int:cat_id>/",views.ParticularCategoriesSubCategoriesTable.as_view()),
    path("all-sub-categories/",views.AllSubCategories.as_view()),
    path("edit-sub-category/<int:sub_cat_id>/",views.EditSubCategory.as_view()),
    path("delete-sub-category/<int:sub_cat_id>/",views.DeleteSubCategory.as_view()),
    # Products
    path("add-product/",views.AddProduct.as_view()),
    path("add-product-images-colors/",views.AddProductImagesColors.as_view()),
    path("particular-products-images-colors/<int:product_id>/",views.ParticularProductColorsAndImages.as_view()),
    path("all-products/",views.AllProducts.as_view()),
    path("particular-category-products/<int:cat_id>/",views.ParticularCategoryProducts.as_view()),
    path("product-details/<int:product_id>/",views.ProductDetails),
    path("edit-product/<int:product_id>/",views.EditProduct.as_view()),
    path("delete-product-images-colors/<int:prod_img_id>/",views.DeleteParticularProductImage.as_view()),
    path("delete-product/<int:product_id>/",views.DeleteProduct.as_view()),

    path("deleted-products/",views.DeletedProducts.as_view()),

    # General APIs
    path('states/', views.StatesList.as_view()),
    path('create-states/', views.CreateStates.as_view()),
    path('districts/<int:state_id>/', views.DistrictsList.as_view()),
    path('all-districts/', views.AllDistrictsDetailedView.as_view()),
    path('create-districts/', views.CreateDistrictsList.as_view()),
    path('mandals/<int:district_id>/', views.MandalsList.as_view()),
    path('create-mandals/', views.CreateMandals.as_view()),
    path('all-mandals/', views.AllMandalsDetailedView.as_view()),
    # Stories
    path('add-story/', views.AddHighlightStories.as_view()),
    path('delete-story/<int:story_id>/', views.DeleteHighlightStories.as_view()),
    path('all-stories/', views.AllHighlightStories.as_view()),
    path('edit-story/<int:story_id>/',views.EditStory.as_view()),
    path('particular-story/<int:story_id>/',views.ParticularHighlightStory.as_view()),
    # Banners
    path('add-banner/',views.AddBanner.as_view()),
    path('all-banner/',views.AllBanner.as_view()),
    path('delete-banner/<int:banner_id>/', views.DeleteBanner.as_view()),
    path('edit-banner/<int:banner_id>/', views.EditBanner.as_view()),
    path('particular-banner/<int:banner_id>/',views.ParticularBannerDetails.as_view()),
    # Chats
    path('all-users-in-chats/',views.AllUsersInChats.as_view()),
    path('particular-users-chat/<str:user_id>/',views.ParticularUsersChats.as_view()),
    path('reply-to-chat/',views.ChatWithUsReply.as_view()),
    path('particular-chat-all-replies/<int:chat_id>/',views.ParticularChatAllReplies.as_view()),
    # Users
    path('particular-user-details/<str:user_id>/',views.ParticularUserDetails.as_view()),
    # Coupons
    path("add-coupons/",views.AddCoupon.as_view()),
    path("get-coupons/",views.GetCoupons.as_view()),
    path("get-coupon-details/<int:coupon_id>/",views.ParticularCouponDetails),
    path("edit-coupon-details/<int:coupon_id>/",views.EditCouponDetails.as_view()),
    path("delete-coupon/<int:coupon_id>/",views.DeleteCoupon.as_view()),
    # Analytics
    path("more-in-wishlist/",views.MoreInWishlist.as_view()),
    path("orders-data-for-dashboard/",views.OrdersDataForDashboard.as_view()),

    # All Orders
    path("all-orders/",views.AllOrders.as_view()),
    path("particular-order-details/<int:order_id>/",views.ParticularOrderDetails),
    # path("manage-order/<int:order_id>/",views.ManageOrder.as_view()),
    # Hurry up products
    path("products-lessthan-10-quantity/",views.HurryUpProducts.as_view()),
    # Handle Order Status
    path("order-confirmed/<int:order_id>/",views.OrderConfirmed.as_view()),
    path("order-shipped/<int:order_id>/",views.OrderShipped.as_view()),
    path("order-on-the-way/<int:order_id>/",views.OrderOnTHeWay.as_view()),
    path("order-delivered/<int:order_id>/",views.OrderDelivered.as_view()),
    path("order-returned/<int:order_id>/",views.OrderReturned.as_view()),
    path("order-cancelled/<int:order_id>/",views.OrderCancelled.as_view()),
    # Top Selling Products
    path("top-selling-products/",views.TopSellingProducts.as_view()),
    # All users
    path("all-users/",views.AllUsers.as_view()),



    # #############################################################################   Phase - 2   #############################################################################
    # Customizer Fonts
    path("add-fonts/",views.AddFontsAPIView.as_view()),
    path("edit-font/<int:font_id>/",views.EditFontsAPI.as_view()),
    path("delete-font/<int:font_id>/",views.DeleteCustomizerFonts.as_view()),
    path("all-fonts/",views.AllCustomizerFonts.as_view()),
    # Customizer Emoji
    path("add-emoji/",views.AddEmojisAPIView.as_view()),
    path("edit-emoji/<int:emoji_id>/",views.EditEmojiAPI.as_view()),
    path("delete-emoji/<int:emoji_id>/",views.DeleteCustomizerEmoji.as_view()),
    path("all-emojis/",views.AllCustomizerEmojis.as_view()),
    # Customizer Colors
    path("add-colors/",views.AddCustomizerColorAPIView.as_view()),
    path("edit-color/<int:color_id>/",views.EditCustomizerColorAPI.as_view()),
    path("delete-color/<int:color_id>/",views.DeleteCustomizerColor.as_view()),
    path("all-colors/",views.AllCustomizerColors.as_view()),
    # Customizer Shapes
    path("add-shape/",views.AddCustomizerShapeAPIView.as_view()),
    path("edit-shape/<int:shape_id>/",views.EditCustomizerShapeAPI.as_view()),
    path("delete-shape/<int:shape_id>/",views.DeleteCustomizerShape.as_view()),
    path("all-shapes/",views.AllCustomizerShapes.as_view()),
    # Customizer Bacground images
    path("add-background-image/",views.AddCustomizerBackgroundImages.as_view()),
    path("edit-cusomizer-background-image/<int:backgroud_img_id>/",views.EditCustomizerBackgroundImage.as_view()),
    path("delete-customizer-background-image/<int:background_img_id>/",views.DeleteCustomizerBackgroundImage.as_view()),
    path("all-background-images/",views.AllCustomizerBackgroundImages.as_view()),
    # Customizer Dimensions
    path("add-dimension/",views.AddCustomizerDimensionsAPIView.as_view()),
    path("edit-dimension/<int:dimension_id>/",views.EditCustomizerDimensionsAPI.as_view()),
    path("delete-dimension/<int:dimension_id>/",views.DeleteCustomizerDimension.as_view()),
    path("all-dimensions/",views.AllCustomizerDimensions.as_view()),

    # Customizable Templates
    path("all-customizable-templates/",views.GETAllCustomizableTemplates.as_view()),
    path("add-template/",views.AddNewTemplate.as_view()),
    path("edit-template/<int:template_id>/",views.EditCustomizableTemplate.as_view()),
    path("delete-template/<int:template_id>/",views.DeleteCustomizableTemplate.as_view()),

    # Customizer Orders
    path("all-customizer-orders/",views.AllCustomizerOrders.as_view()),
    path("particular-customizer-order-details/<int:order_id>/",views.ParticularCustomizerOrderDetails),
    # Handle Customizer Order Status
    path("customizer-order-confirmed/<int:order_id>/",views.CustomizerOrderConfirmed.as_view()),
    path("customizer-order-shipped/<int:order_id>/",views.CustomizerOrderShipped.as_view()),
    path("customizer-order-on-the-way/<int:order_id>/",views.CustomizerOrderOnTHeWay.as_view()),
    path("customizer-order-delivered/<int:order_id>/",views.CustomizerOrderDelivered.as_view()),
    path("customizer-order-returned/<int:order_id>/",views.CustomizerOrderReturned.as_view()),
    path("customizer-order-cancelled/<int:order_id>/",views.CustomizerOrderCancelled.as_view()),


    # Logo Orders
    path("all-logo-orders/",views.AllLogoTemplateOrders.as_view()),
    path("particular-logo-order-details/<int:order_id>/",views.ParticularLogoTemplateOrderDetails),






]

