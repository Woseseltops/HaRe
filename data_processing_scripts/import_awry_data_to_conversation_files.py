from json import load

ROOT = '../datasets/conversations_gone_awry/'
SOURCE = ROOT+'paired_conversations.json'
current_conversation = ''
toxic_users_this_conversation = set()
outputfile = open(ROOT+'conversations.txt','w')

for comment in load(open(SOURCE)):

    if '==' in comment['text']:
        continue

    username = comment['user'].replace(' ','_')
    text = comment['text'].replace('\n',' [LINEBREAK] ')

    if comment['awry_info']['page_title'] != current_conversation:

        if len(toxic_users_this_conversation) > 0:
            outputfile.write('# toxic '+str(list(toxic_users_this_conversation)[0])+'\n\n')

        toxic_users_this_conversation = set()
        current_conversation = comment['awry_info']['page_title']

        if len(toxic_users_this_conversation) > 1:
            print('!')

    outputfile.write(username+'\t'+text+'\n')

    if comment['awry_info']['comment_has_personal_attack']:
        toxic_users_this_conversation.add(username)

outputfile.write('# toxic '+str(list(toxic_users_this_conversation)[0])+'\n\n')