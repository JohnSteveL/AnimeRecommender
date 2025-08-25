from utils.helper import *
from config.path_config import *
from pipeline.prediction_pipeline import hybrid_recommendation

#similiar_users=find_similiar_user(11880,USER_WEIGHTS_PATH,USER2USER_ENCODED,USER2USER_DECODED)

#user_pref=get_user_preferences(11880,RATING_DF,DF)

#user_recommend=get_user_recommendations(similiar_users,user_pref,DF,RATING_DF,SYNOPSIS_DF)
#print(user_recommend)

#similiar_anime=find_similiar_animes("Fullmetal Alchemist:Brotherhood",ANIME_WEIGHTS_PATH,ANIME2ANIME_ENCODED,ANIME2ANIME_DECODED,DF,SYNOPSIS_DF)
#print(similiar_anime)

print(hybrid_recommendation(11880))