import base64
import json
import urllib2
import pprint
import sys


def get_from_api_jira(a_list):
    """
    ***Enter your Jira username and password on the variables***

    Get data from Jira ticket for each Jira ticket number on a_list
    return tuple with Desk ticket number, Jira ticket number, status and fixVersion if Jira status is Resolved
    :param a_list: list with Desk numner and Jira number
    :return: tuple
    """
    result = ()
    for elem in a_list:
        try:
            base_url = "https://trainingrocket.atlassian.net/rest/api/latest/issue/"
            api_call = base_url + elem[1]
            request = urllib2.Request(api_call)
            username = ''  # <-------- Enter username between the ''
            password = ''  # <---------- Enter password between the ''
            base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
            request.add_header("Authorization", "Basic %s" % base64string)
            json_obj = urllib2.urlopen(request)
            data = json.load(json_obj)
            status = data['fields']['status']['name']
            fix_versions = data['fields']['fixVersions']
            if str(status) == 'Resolved':
                fix_versions = str(fix_versions[0]['name'])
                list_with_info = [elem[0], elem[1], str(status), str(fix_versions)]
                result += (list_with_info,)
        except:
            print 'Could not find ' + elem[1] + ' On Desk ticket: ' + elem[0] + ' please review manually'
            continue
    return result


def get_from_api_desk():
    """
    ***Enter your Desk username and password and your name below***
    Get a list of Desk cases that are assigned to Dev with the Jira Ticket IDs
    :return:  list
    """
    try:
        result = []
        base_url = "https://servicerocket.desk.com/api/v2/cases/search?q=status:pending%20custom_status:%22Assigned%20to%20DEV%22%20assigned:%22"
        engineer_name = ''  # <----- Enter your name
        engineer_name = engineer_name.split()
        for name in engineer_name[:-1]:
            base_url += name + '%20'
        base_url += engineer_name[-1] + '%22'
        request = urllib2.Request(base_url)
        username = ''  # <---- Enter your Desk username
        password = ''  # <------ Enter you Desk password
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        json_obj = urllib2.urlopen(request)
        data = json.load(json_obj)
        for elem in data['_embedded']['entries']:
            desk_id = str(elem['id'])
            jira_id = str(elem['custom_fields']['jira_id'])
            result.append([desk_id, jira_id])
        return result
    except:
        print 'Could not connect to Desk. Check if usernmae and password are correct'
        sys.exit()


desk_info = get_from_api_desk()
result = get_from_api_jira(desk_info)
print
print 'Final Results:'
print '=============='
print
if result == ():
    print 'Nothing to check =)'
else:
    pprint.pprint(result)
