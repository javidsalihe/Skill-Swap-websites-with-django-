from django.urls import path

from skill.views import skill, skillCategory, userSkill, exchange, search, skillSwap, rate

urlpatterns = [
    path('skillCategories', skillCategory.skill_category_list, name="skill_category_list"),
    path('skillCategories/create/', skillCategory.create_skill_category, name='create_skill_category'),
    path('skillCategories/update/<int:pk>/', skillCategory.update_skill_category, name='update_skill_category'),
    path('skillCategories/delete/<int:pk>/', skillCategory.delete_skill_category, name='delete_skill_category'),

    path('skills', skill.skill_list, name="skill_list"),
    path('skills/create/', skill.create_skill, name='create_skill'),
    path('skills/update/<int:pk>/', skill.update_skill, name='update_skill'),
    path('skills/delete/<int:pk>/', skill.delete_skill, name='delete_skill'),

    path('userskills', userSkill.user_skill_list, name="user_skill_list"),
    path('userskills/create/', userSkill.create_user_skill, name='create_user_skill'),
    path('userskills/update/<int:pk>/', userSkill.update_user_skill, name='update_user_skill'),
    path('userskills/delete/<int:pk>/', userSkill.delete_user_skill, name='delete_user_skill'),

    path('exchanges', exchange.exchanges, name="exchanges"),
    path('exchanges/create_exchange_request/', exchange.create_exchange_request, name="create_exchange_request"),
    path('exchanges/delete_exchange_request/<int:pk>/', exchange.delete_exchange_request,
         name="delete_exchange_request"),
    path('exchanges/update_exchange_request/<int:pk>/', exchange.update_exchange_request,
         name="update_exchange_request"),

    path('search/searching_result', search.searching_result, name="searching_result"),

    path('exchange_request/<uuid:request_id>/send/', skillSwap.send_exchange_request, name='send_exchange_request'),
    path('swap_skill', skillSwap.swap_skill, name="swap_skill"),
    path('skill_swaping_update/<uuid:exchange_uuid>/', skillSwap.skill_swaping_update, name="skill_swaping_update"),

    path('negotiation/respond/<int:neg_id>/<str:action>/', skillSwap.respond_negotiation, name='respond_negotiation'),
    path('negotiation/delete/<int:neg_id>/', skillSwap.delete_negotiation, name='delete_negotiation'),
    path('negotiation/add/<uuid:exchange_uuid>/', skillSwap.manage_negotiation, name='add_negotiation'),
    path('negotiation/update/<int:neg_id>/', skillSwap.update_negotiation, name='update_negotiation'),

    path('exchange/complete/<uuid:exchange_uuid>/', skillSwap.complete_exchange, name='complete_exchange'),
    path('exchange/<uuid:exchange_uuid>/rate/', skillSwap.rate_exchange, name='rate_exchange'),


    path('skill_swap_details/', skillSwap.skill_swap_details, name="skill_swap_details"),
    path('rating/comment/add/<int:rating_id>/', skillSwap.add_exchange_comment, name="add_exchange_comment"),
# admi all exchange
    path('admin/exchanges/', skillSwap.manage_all_exchanges, name="manage_all_exchanges"),
    path('admin/exchanges/edit/<uuid:exchange_uuid>/', skillSwap.edit_exchange_admin, name="edit_exchange_admin"),
    path('admin/exchanges/delete/<uuid:exchange_uuid>/', skillSwap.delete_exchange_admin, name="delete_exchange_admin"),


    # rate managment
    path('admin/ratings/', rate.manage_ratings, name='manage_ratings'),
    path('admin/ratings/update/<int:pk>/', rate.update_rating, name='update_rating'),
    path('admin/ratings/delete/<int:pk>/', rate.delete_rating, name='delete_rating'),
    path('admin/ratings/toggle/<int:pk>/', rate.toggle_rating_hide, name='toggle_rating_hide'),
    path('admin/ratings/comment/add/<int:rating_id>/', rate.add_admin_reply, name='add_admin_reply'),
    path('admin/ratings/comment/delete/<int:comment_id>/', rate.delete_comment, name='delete_comment'),


]



