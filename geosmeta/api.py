# Copyright (c) The University of Edinburgh, 2014.
#
import tool
import json
import util
import requests

__all__ = ['GeosMETA']

def processGetResponse(response):
    """Utility method to process the requests response
    for get methods.

    :param response: requests response object
    :returns: JSON from response if response contains it
    :raises Exception: if problem processing response
                       or error received from server
    """

    code = requests.codes.ok
    return processResponse(response, code)

def processPostResponse(response):
    """Utility method to process the requests response
    for post methods.

    :param response: requests response object
    :returns: JSON from response if response contains it
    :raises Exception: if problem processing response
                       or error received from server
    """

    code = requests.codes.created
    return processResponse(response, code)

def processResponse(response, statusCode):
    """Utility method to process the requests response.

    :param response: requests response object
    :param statusCode: HTTP status code to check response against
    :returns: JSON from response if response contains it
    :raises Exception: if problem processing response
                       or error received from server
    """

    if response.status_code == statusCode:
        try:
            responseJSON = response.json()
        except ValueError:
            responseJSON = None
        return responseJSON
    else:
        # Gets status codes 4XX and 5XX only

        # moving to seek to hold onto the err message from server
        # as it gives validation errors.
        # response.raise_for_status()

        message = "Status code: %s" %(response.status_code)
        try:
            responseJSON = response.json()
        except Exception:
            responseJSON = None
            response.raise_for_status() # maybe here is not the place...??
        if responseJSON is not None:
# why make a string? just return reponse??? Mike Jan 2016
#...exception at least until python 3 needs a str... 
# could make one we can then interpret back into  json.... ??
            reason = json.dumps(responseJSON) # this not present with 404 code ['_issues'])
            message += "\nReason: " + reason
        raise Exception(message)

class GeosMETA(object):
    def __init__(self, configFilePath = None):
        """Constructor.

        :param configFilePath: The location of the geosmeta configuration
                               file. If not present this defaults to
                               $HOME/.geosmeta/geosmeta.cfg
        """

        # Tool object to talk to the GeosMeta server
        self.tool = tool.Tool(configFilePath=configFilePath)

    def getAccounts(self):
        """Get account details from system.

        :returns: JSON response
        :raises Exception: if problem getting accounts
        """
        message = ''
        resource = 'accounts'
        response = self.tool.performGet(resource, message)

        return processGetResponse(response)

    def getAccount(self,username):
        """Get account details from system for a user.

        :param username: username to lookup
        :returns: JSON response
        :raises Exception: if problem getting accounts
        """
        message = ''
        resource = 'accounts/' + username
        response = self.tool.performGet(resource, message)

        return processGetResponse(response)

    def postAccount(self,accountJSON):
        """Post user account to database.

        :param accountJSON: JSON containing account details
        :returns: requests response object
        """
        return self.tool.performPost('accounts', accountJSON)

    def createUser(self,firstname, lastname, username, email, secret, roles):
        """Create a user in the Geosmeta system

        :param firstname: Firstname of the user
        :param lastname: Lastname of the user
        :param username: Username of the user - becomes id of user doc
        :param email: Email of the user
        :param secret: Secret key
        :param roles: List of roles
        :returns: id of user if creation successful
        :raises Exception: if problem creating user
        """
        account = {'_id': username,
                   'firstname': firstname,
                   'lastname': lastname,
                   'email': email,
                   'secret': secret,
                   'roles': roles
                   }
        response = self.postAccount(json.dumps(account))

        return processPostResponse(response)

    def getProjectRoles(self,project_id):
        """Get the roles for a project.
        :param project_id: project to get roles from
        :returns: JSON response
        :raises Exception: if problem getting the document
        """

        message = ''
        resource = 'project_roles/%s'%project_id
        #+ projectName
#        params = {'where': '{"project": "' +  project_id + '"}' }
        response = self.tool.performGet(resource, message)#, params)

        return processGetResponse(response)

    def fromAbbrevToResource(self, abbrev):
        if abbrev=="A":
            resource = 'activities'
        elif abbrev=="F":
            resource= 'gmfiles'
        elif abbrev=="E":
            resource= 'entities'
            print("entities not in use - Stopping.")
            sys.exit()
        else:
            print("bad collection specified")
            sys.exit()
        return resource

    def getDoc(self,collection,projectName, id,  selectedFields=None, verbose=False):
        """Get a document.
        :param collection
        :param projectName: project to get activity from
        :param id: id to retrieve
        :returns: JSON response
        :raises Exception: if problem getting the document
        """
        if projectName ==None:
                  projectName=self.tool.config._projectname

        message = ''
        params= ''
        resource = "%s/%s"%(self.fromAbbrevToResource(collection), id)
            
        hdr_ext={"project": projectName} 
        if selectedFields:
             hdr_ext["selectedFields"]=selectedFields
        if verbose:
            print(resource)
            print(params)
            print(message)
        response = self.tool.performGet(resource, message, hdr_ext=hdr_ext)

        return processGetResponse(response)
    def getActivity(self, projectName, id):
        return self.getDoc("A",projectName, id)
        

    def getProjectCollection(self,collection,projectName, selectedFields=None):
        """Get all collection's documents for a given project.
        :param projectName: project to get activities from
        :returns: JSON response
        :raises Exception: if problem getting the document
        """
        if projectName ==None:
                  projectName=self.tool.config._projectname

        resource = self.fromAbbrevToResource(collection)

        hdr_ext={"project": projectName} 
        if selectedFields:
             hdr_ext["selectedFields"]=selectedFields
        message = ''
        params = {'where': '{"project": "' + projectName + '"}'}
        #print params
        response = self.tool.performGet(resource, message, params=params, hdr_ext=hdr_ext)

        return processGetResponse(response)

    def getHREF(self,href, projectName,selectedFields=None, verbose=False):
        """Get all activity documents for a given project.
        :returns: JSON response
        :raises Exception: if problem getting the document
        """
#        import pdb; pdb.set_trace()
        message = ''
        resource = href.split('?')[0] #'activities'
        params =href.split('?')[1]
        if verbose:
            print("getHREF params: "+params)
            print("resource:" + resource)
        if projectName ==None:
                  projectName=self.tool.config._projectname

        hdr_ext={"project": projectName}
        if selectedFields:
             hdr_ext["selectedFields"]=selectedFields

        response = self.tool.performGet(resource, message, params,hdr_ext)

        return processGetResponse(response)
    
    def findActivities(self,collection, projectName, query, kwargs):
        """Find/search activity documents in the project that satisfies the query .
        :param projectName: project to get activities from
        :param query: query parameters
        :returns: JSON response
        :raises Exception: if problem getting the documents
        """
        if projectName ==None:
                  projectName=self.tool.config._projectname

        hdr_ext={"project": projectName} 
        if kwargs:
          if 'selectedFields' in kwargs:
             hdr_ext["selectedFields"]=kwargs["selectedFields"]
          if 'summary' in kwargs:
              hdr_ext["summaryOnly"]='T'
#        print "hdr_ext "+str(hdr_ext)
        message = ''
        resource = self.fromAbbrevToResource(collection)

        params = {'where': '{"$and":[{"project": "' + projectName + '"},{' + query + '}]}'}
        print(params)

        response = self.tool.performGet(resource, message,
                                         params=params, hdr_ext=hdr_ext)
        return processGetResponse(response)


    def findFileUse(self,projectName,filename,testField):
        """ Look for filename in the specified list (in/output_files)
            and return the number and ids of docs that have
            status of Current
        """
        if testField == "input_file_docs" or testField =="output_file_docs":
           query='"$and":[{"%s.filename":"%s"}]'%(testField,filename)
           kwargs={'summaryOnly':'T'}
           opdict=self.findActivities('A',projectName, query, kwargs)
		# assuming not more than 25 docs returned as not handling that.
           currentList=list()
           for iitem in opdict["_items"]:
              if iitem:
                 if iitem["gmstatus"] == "Current":
                    currentList.append(iitem["_id"])       
           return opdict["_meta"]["total"], currentList
           
        else:
           print("bad argument to findFileUse")
           print("must be 'input_files' or 'output_files'")
           return -1,[]


    def getProject(self,project_id=None):
        """Get projects from the database.
        :param project_id: project to get details for (optional)
        :returns: JSON response
        :raises Exception: if problem getting the project
        """

        message = ''
        if project_id ==None:
                  project_id=self.tool.config._projectname

        resource = 'projects/%s'%project_id
        response = self.tool.performGet(resource, message)

        return processGetResponse(response)

    def getProjects(self,project_id=None, researchGroupName=None):
        """Still in use?? Get projects from the database.
        :param project_id: project to get details for (optional)
        :param researchGroupName: research group to get details for (optional)
        :returns: JSON response
        :raises Exception: if problem getting the project
        """

        message = ''
        resource = 'projects'
        if project_id ==None:
                  project_id=self.tool.config._projectname
        if project_id is None:
            if researchGroupName is None:
                params = None
            else:
                params = {'where': '{"research_group": "' + researchGroupName +'"}'}
        else:
            if researchGroupName is None:
                params = {'where': '{"title": "' + projectName +'"}'}
            else:
                params = {'where': '{"research_group": "' + researchGroupName
                            + '", "title": "' + projectName + '"}'}

        response = self.tool.performGet(resource, message, params)

        return processGetResponse(response)

    def getResearchGroups(self,researchGroupName=None):
        """Get Research Groups from the database.
        :param researchGroupName: research group to get details for (optional)
        :returns: JSON response
        :raises Exception: if problem getting the project
        """

        message = ''
        resource = 'research_groups'
        if researchGroupName is None:
            params = None
        else:
            params = {'where': '{"title": "' + researchGroupName +'"}'}

        response = self.tool.performGet(resource, message, params)

        return processGetResponse(response)
    
    def postResearchGroup(self,researchGroupJSON):
        return self.tool.performPost('research_groups', researchGroupJSON)

    def addResearchGroup(self,title, description, comment):
        """ Adds a new research group

        :param title: Unique (required) title of the research group
        :param description: Description of research group
        :param comment: Comment
        :return: id of the research group if created successfully
        """
        creator = self.tool.config.username

        research_group = {'title': title,
                          'creator': creator}

        if description is not None:
            research_group['shortDescription'] = description

        if comment is not None:
            research_group['comment'] = comment

        response = self.postResearchGroup(json.dumps(research_group))

        return processPostResponse(response)

    def postProject(self,projectJSON):
        return self.tool.performPost('projects', projectJSON)

    def postProjectRoles(self,projectRolesJSON):
        return self.tool.performPost('project_roles', projectRolesJSON)

    def addProject(self,project_id, researchGroup, description, comment):
        """ Adds a new project

        :param project_id: Unique title of the project (required, no spaces allowed)
        :param researchGroup: Name of research group to add project to
        :param description: Description of project
        :param comment: Comment
        :return: id of the project if created successfully
        """
        creator = self.tool.config.username

        project = {'_id': project_id,
                   'research_group': researchGroup,
                   'creator': creator}

        if description is not None:
            project['shortDescription'] = description

        if comment is not None:
            project['comment'] = comment

        response = self.postProject(project )#json.dumps(project))

        processPostResponse(response)

        response_json = response.json()
        if response_json['_status'] == "OK":
            project_roles = {'_id': project_id,
                         'read_access': [],
                         'write_access': []}

            responseRoles = self.postProjectRoles(project_roles)#json.dumps(project_roles))

            processPostResponse(responseRoles)

            response_json = responseRoles.json()
            if response_json['_status'] == "OK":
                id = response_json['_id']
                return id
            else:
                raise Exception("Roles Status not OK")
        else:
            raise Exception("New project status not OK")

    def postActivity(self,activityJSON):
        return self.tool.performPost('activities', activityJSON)

    def patchActivity(self,resource, changesJSON, etag):
        return self.tool.performPatch(resource, changesJSON, etag)

    def updateDocStatus(self,activityID, etag, newStatus, message,goDownStream):
        """ Updates a gmDoc's status field, and optionally change status
recirsively down the tree
        :param activityID: _id of the gmDoc to be changed
        :param etag: correct _etag of the current document
        :param newStatus: C(urretn) or E(rror)
        :param message: brief description of why status is changed
        :param goDownStream: True if all docs downstream of this are to have
new status
        :return: id of the activity if update successful
        """
        import time
        stati={'C':"Current",'E':"Error"} # already validated.
        resource = 'activities/' + activityID

        changes = {'statNew':
                         {'message':message,
                          "status":stati[newStatus],
                          "byWhom":self.tool.config.username,
                          "goDownStream":goDownStream}}

        changesJSON = json.dumps(changes)

        return self.patchActivity(resource, changesJSON, etag)


    def updateActivity(self,activityID, etag, field, value):
        """ Updates an activity field with a value provided.
        :param activityID: _id of the activity document to be changed
        :param etag: correct _etag of the current document
        :param field: field to be changed
        :param value: new value for the field
        :return: id of the activity if update successful
        """

        resource = 'activities/' + activityID
        changes = {field: value}
        changesJSON = json.dumps(changes)

        return self.patchActivity(resource, changesJSON, etag)

    def addDoc(self,project, metaFields):
        """ Adds a new document

        :param project: optional: Project the activity is associated with
        :param metaFields: A valid JSON file or a python dict
        :return: id of the activity document if created successfully
        """
        creator = self.tool.config.username

        if isinstance(metaFields,str):
          with open(metaFields) as theFile:
            theContent = json.load(theFile)
        elif isinstance(metaFields,dict):
             theContent = metaFields
        else:
               response = "cant use argument metaFields: Not JSON file or python dict - quitting"
               return response
        
        if project ==None:
                  project=self.tool.config._projectname

        activity = { 'project': project,
                    'creator': creator,
                    'gmstatus': "Current", 
                              # it has to be current if we are writign it!
                    'gmdata': theContent} 
        response = self.postActivity(activity)#json.dumps(activity))

        return processPostResponse(response)

