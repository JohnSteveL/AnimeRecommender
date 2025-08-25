from config.path_config import *
from utils.helper import *

def hybrid_recommendation(user_id,n=10,user_weight=0.5, content_weights=0.5):
    
    ## user recommendation
    similar_users = find_similiar_user(user_id,USER_WEIGHTS_PATH,USER2USER_ENCODED,USER2USER_DECODED)
    user_pref = get_user_preferences(user_id,RATING_DF,DF)
    user_recommended_animes = get_user_recommendations(similar_users,user_pref,DF,RATING_DF,SYNOPSIS_DF)

    user_recommended_anime_list = user_recommended_animes["anime_name"].tolist()
    

    ## content recommendation
    content_recommended_animes = []

    for anime in user_recommended_anime_list:
        
        similar_animes = find_similiar_animes(str(anime),ANIME_WEIGHTS_PATH,ANIME2ANIME_ENCODED,ANIME2ANIME_DECODED,DF,SYNOPSIS_DF)

        if similar_animes is not None and not similar_animes.empty:
            content_recommended_animes.extend(similar_animes["name"].tolist())
        else:
            print(f"No similar anime found {anime}")
        
    combined_scores = {}

    for anime in user_recommended_anime_list:
        combined_scores[anime] = combined_scores.get(anime,0) + user_weight

    for anime in content_recommended_animes:
        combined_scores[anime] = combined_scores.get(anime,0) + content_weights
    
    sorted_animes = sorted(combined_scores.items() , key=lambda x:x[1] ,reverse=True )

    final_recommendations = []
    for anime, _ in sorted_animes[:n]:
        synopsis = getSynopsis(anime,SYNOPSIS_DF)
        final_recommendations.append({
            "anime": anime,
            "synopsis": synopsis
        })
    
    return final_recommendations
