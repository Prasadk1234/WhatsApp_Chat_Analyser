import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whats Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    # user_list.remove('No One')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages, words, num_media_messages = helper.fetch_stats(selected_user, df)

        st.title("Analysis")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)


        # timeline

        st.title('Monthly Timeline graph')
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Activity map
        st.title('Activity amp')
        col1, col2 = st.columns(2)

        with col1:
            st.header('Most busy day')
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(busy_day.index, busy_day.values)
            st.pyplot(fig)

        with col2:
            st.header('Most busy month')
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(busy_month.index, busy_month.values, color='red')
            st.pyplot(fig)

        st.title("Weekly Heatmap for chat")
        user_heatmap = helper.acitivity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # Word Cloud
        st.title('Word Cloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title('Most common Words')
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')

        st.pyplot(fig)

        """# emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.dataframe(emoji_df)"""

