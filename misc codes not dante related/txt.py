import requests
post_data = {
                'model':'/var/workflow/models/pwc-express-publish-review-page-workflow',
                '_charset_':'utf-8',
                'payload':'/content/pwc/rm/en/testpage',
                'payloadType':'JCR_PATH',
                'workflowTitle':"From PC"
                }
post_url = 'https://dpe-qa.pwc.com/var/workflow/instances'
post_resp_data = requests.post(post_url, data=post_data, auth=("chiranjib.bhattacharyya@in.pwc.com", "Change@123456"))
print(post_resp_data.status_code)