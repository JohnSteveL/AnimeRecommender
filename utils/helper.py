import pandas as pd
import numpy as np
import joblib
from config.path_config import *

###### 1. Anime Frame

def getAnimeFrame(anime,path_df):
    df = pd.read_csv(path_df)
    if isinstance(anime,int):
        return df[df.anime_id == anime]
    if isinstance(anime,str):
        return df[df.eng_version == anime]


###### 2. Synopsis

def getSynopsis(anime,path_synopsis_df):
    syn_df = pd.read_csv(path_synopsis_df)
    if isinstance(anime, int):
        result = syn_df[syn_df.MAL_ID == anime]
        if not result.empty:
            return result.sypnopsis.values[0]
    elif isinstance(anime, str):
        result = syn_df[syn_df.eng_version == anime]
        if not result.empty:
            return result.sypnopsis.values[0]
    return None
    

##### 3. Content Recommendation

def find_similiar_animes(name,path_anime_weights,path_anime2anime_encoded,
                         path_anime2anime_decoded,path_df,path_synopsis_df,n=10,return_dist=False,neg=False):
    
    anime_weights = joblib.load(path_anime_weights)
    anime2anime_encoded = joblib.load(path_anime2anime_encoded)
    anime2anime_decoded = joblib.load(path_anime2anime_decoded)
    df = pd.read_csv(path_df)
    syn_df = pd.read_csv(path_synopsis_df)

    index = getAnimeFrame(name,path_df).anime_id.values[0]
    encoded_index = anime2anime_encoded.get(index)

    weights = anime_weights

    dists = np.dot(weights,weights[encoded_index])
    sorted_dists = np.argsort(dists)

    n=n+1
    
    if neg:
        closest = sorted_dists[:n]
    else:
        closest = sorted_dists[-n:][::-1]
    

    if return_dist:
        return dists,closest
    
    SimilarityArr = []

    for close in closest:
        decoded_id = anime2anime_decoded.get(close)

        

        anime_frame = getAnimeFrame(decoded_id,path_df)
        synopsis = getSynopsis(decoded_id,path_synopsis_df)
        anime_name = anime_frame.eng_version.values[0]
        genre = anime_frame.Genres.values[0]
        similarity = dists[close]

        SimilarityArr.append({
            "anime_id" : decoded_id,
            "name" : anime_name,
            "similarity" : similarity,
            "genre" : genre,
            "synopsis" : synopsis
            
        })

    Frame = pd.DataFrame(SimilarityArr).sort_values(by="similarity",ascending=False)
    return Frame[Frame.anime_id != index].drop(["anime_id"],axis=1)

##### 4. Similiar Users

def find_similiar_user(item_input, path_user_weights,path_user2user_encoded,
                       path_user2user_decoded,n=10,return_dist=False,neg=False):
    
    user_weights = joblib.load(path_user_weights)
    user2user_encoded = joblib.load(path_user2user_encoded)
    user2user_decoded = joblib.load(path_user2user_decoded)

    index = int(item_input)
    encoded_index = user2user_encoded.get(index)
    weights = user_weights

    if encoded_index is not None:

        dists = np.dot(weights,weights[encoded_index])
        sorted_dists = np.argsort(dists)

        n=n+1
        
        if neg:
            closest = sorted_dists[:n]
        else:
            closest = sorted_dists[-n:][::-1]
        

        if return_dist:
            return dists,closest
        
        SimiliarityArr = []

        for close in closest:
            similarity = dists[close]

        
            decoded_id = user2user_decoded.get(close)
            SimiliarityArr.append({
                "similiar_users" : decoded_id,
                "similarity" : similarity,
                
            })
            
            sim_users = pd.DataFrame(SimiliarityArr).sort_values(by="similarity",ascending=False) 
            sim_users = sim_users[sim_users.similiar_users != item_input]
        return sim_users


###### 5. User Preferences

def get_user_preferences(user_id, path_rating_df,path_df, verbose=0, plot=False ):
    
    rating_df = pd.read_csv(path_rating_df)
    df = pd.read_csv(path_df)

    animes_watched_by_user = rating_df[rating_df.user_id == user_id]

    if not animes_watched_by_user.rating.empty:
        user_rating_percentile = np.percentile(animes_watched_by_user.rating , 75)
    else:
        user_rating_percentile = np.nan


    animes_watched_by_user = animes_watched_by_user[animes_watched_by_user.rating >= user_rating_percentile]

    top_animes_user = (
        animes_watched_by_user.sort_values(by="rating",ascending=False).anime_id.values
    )

    anime_df_rows = df[df["anime_id"].isin(top_animes_user)]
    anime_df_rows = anime_df_rows[["eng_version","Genres"]]

    
    

    return anime_df_rows


##### 6. User Recommendation

def get_user_recommendations(similar_users,user_pref,path_df,path_rating_df,path_syn_df,n=10):

    rating_df = pd.read_csv(path_rating_df)
    df = pd.read_csv(path_df)
    syn_df = pd.read_csv(path_syn_df)
    
    recommended_animes = []
    anime_list = []

    for user_id in similar_users.similiar_users.values:
        pref_list = get_user_preferences(user_id,path_rating_df,path_df)

        pref_list = pref_list[~pref_list.eng_version.isin(user_pref.eng_version.values)]

        if not pref_list.empty:
            anime_list.append(pref_list.eng_version.values)

    if anime_list:
        anime_list = pd.DataFrame(anime_list)

        sorted_list = pd.DataFrame(pd.Series(anime_list.values.ravel()).value_counts()).head(n)

        for i,anime_name in enumerate(sorted_list.index):
            n_users_pref = sorted_list[sorted_list.index == anime_name].values[0][0]

            if isinstance(anime_name,str):
                frame = getAnimeFrame(anime_name,path_df)
                genre = frame.Genres.values[0]
                synopsis = getSynopsis(anime_name,path_syn_df)

                recommended_animes.append({
                    "n" : n_users_pref,
                    "anime_name" : anime_name,
                    "Genres": genre,
                    "synopsis" : synopsis
                })
    return pd.DataFrame(recommended_animes).head(n)

               
#### 
    