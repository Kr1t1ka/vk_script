import vk_api
import time


token = 'your_token'


def get_dialog(VkSession, offset=0, filter='all', count=200):
    return VkSession.method('messages.getConversations', {
        'offset': offset,
        'count': count,
        'filter': filter
    })


def get_history(VkSession, user_id, offset=0, count=200, extended=1):
    return VkSession.method('messages.getHistory', {
        'offset': offset,
        'user_id': user_id,
        'count': count,
        'extended': extended
    })


def get_user(VkSession, user_id):
    return VkSession.method('users.get', {
        'user_ids': user_id
    })


def main():
    vk_session = vk_api.VkApi(token=token)
    dict_rating = {}
    dialogs = get_dialog(VkSession=vk_session)
    start_data = 1588280400  # 1588280400 - Fri May  1 00:00:00 2020

    for dialog in dialogs['items']:
        if dialog['last_message']['date'] < start_data:
            break
        user_messages = get_history(VkSession=vk_session, user_id=str(dialog['conversation']['peer']['id']))
        for message in user_messages['items']:
            if ('admin_author_id' in message) and (message['date'] > start_data):
                admin_name = get_user(VkSession=vk_session, user_id=message['admin_author_id'])
                admin_text_name = admin_name[0]['first_name'] + ' ' + admin_name[0]['last_name']
                if admin_text_name not in dict_rating:
                    dict_rating[admin_text_name] = 1
                else:
                    dict_rating[admin_text_name] += 1

    print(dict_rating)


if __name__ == '__main__':
    main()
