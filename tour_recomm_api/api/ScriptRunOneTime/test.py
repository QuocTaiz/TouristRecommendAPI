import pandas as pd

df = pd.read_csv('D:\TaiLieu\DATT\\final_data.csv')

def get_recommend(df, neig_name, LIMIT=5):
        user_rated_venues = df[df['Neighbourhood'] == neig_name]

        user_rated_onehot = pd.get_dummies(user_rated_venues[['Venue Category']], prefix="", prefix_sep="")
        user_rated_onehot['Neighbourhood'] = user_rated_venues['Neighbourhood'] 
        fixed_columns = [user_rated_onehot.columns[-1]] + list(user_rated_onehot.columns[:-1])
        final_grouped = user_rated_onehot.groupby(['Neighbourhood'], sort=False).sum()

        usermatrix = final_grouped.reset_index(drop=True)

        rating_df=user_rated_venues[['Neighbourhood','rating']]
        rating_df['rating']=rating_df['rating'].astype('float')

        rating_grouped=rating_df.groupby('Neighbourhood', sort=False)['rating'].mean()
        rating_df_new=pd.DataFrame(rating_grouped)
        rating_df_new=rating_df_new.reset_index()
        userProfile = usermatrix.transpose().dot(rating_df_new['rating'])

        final_data_onehot = pd.get_dummies(df[['Venue Category']], prefix="", prefix_sep="")
        final_data_onehot['Neighbourhood'] = df['Neighbourhood']
        fixed_columns = [final_data_onehot.columns[-1]] + list(final_data_onehot.columns[:-1])
        neig_grouped=final_data_onehot.groupby(['Neighbourhood'], sort=False).sum()

        recommendationTable_df = ((neig_grouped*userProfile).sum(axis=1))/(userProfile.sum())
        recommendationTable_df = recommendationTable_df.sort_values(ascending=False)
        top = pd.DataFrame(recommendationTable_df).reset_index()
        top.columns=['Neighbourhood','Recommendation']
        return top.head(LIMIT)

df_recommend = get_recommend(df, 'Văn Miếu - Quốc Tử Giám')
print(df_recommend['Neighbourhood'][0])